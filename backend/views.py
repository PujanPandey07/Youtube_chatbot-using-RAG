from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import VideoSession, ChatMessage
from .forms import LoginForm, ChatMessageForm

from rag_components.Chains import build_retriever, create_chain
from rag_components.transcript import extract_video_id, TranscriptError


# -------------------------
# LOGIN / REGISTER
# -------------------------
def login_or_register(request):

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")

            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username, password=password)
                login(request, user)
                return redirect("home")

            return render(request, "backend/login.html", {
                "form": form,
                "error": "Invalid password"
            })

    else:
        form = LoginForm()

    return render(request, "backend/login.html", {"form": form})


# -------------------------
# LOGOUT
# -------------------------
@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


# -------------------------
# MAIN CHAT VIEW (HOME)
# -------------------------
@login_required
def chat_view(request):

    all_sessions = VideoSession.objects.filter(user=request.user)

    session_id = request.GET.get("session") or request.POST.get("session")
    active_session = None
    chat_messages = []
    error = None

    if session_id:
        try:
            active_session = all_sessions.get(id=session_id)
            chat_messages = active_session.messages.all()
        except VideoSession.DoesNotExist:
            active_session = None

    if request.method == "POST":
        video_url = request.POST.get("video_url", "").strip()
        user_message = request.POST.get("user_message", "").strip()

        if video_url and user_message:
            video_id = extract_video_id(video_url)

            if not video_id:
                error = "Invalid YouTube URL. Please check and try again."
            else:
                session = None
                try:
                    session, created = VideoSession.objects.get_or_create(
                        user=request.user,
                        video_id=video_id,
                        defaults={"video_url": video_url}
                    )

                    retriever = build_retriever(video_url)
                    chain = create_chain(retriever)
                    answer = chain.invoke(user_message)

                    ChatMessage.objects.create(
                        session=session,
                        user_message=user_message,
                        bot_response=answer
                    )

                    return redirect(f"{request.path}?session={session.id}")

                except TranscriptError as e:
                    if session and session.messages.count() == 0:
                        session.delete()
                    error = str(e)

                except Exception as e:
                    error = f"Something went wrong: {str(e)}"

    return render(request, "backend/home.html", {
        "all_sessions": all_sessions,
        "active_session": active_session,
        "chat_messages": chat_messages,
        "error": error,
    })
