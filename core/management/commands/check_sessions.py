from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

class Command(BaseCommand):
    help = 'Display all session data'

    def handle(self, *args, **options):
        sessions = Session.objects.all()

        for session in sessions:
            session_data = SessionStore(session_key=session.session_key)
            try:
                session_data.load()
                self.stdout.write(self.style.SUCCESS(f'Session ID: {session.session_key}'))
                self.stdout.write(self.style.SUCCESS(f'Session Data: {session_data._get_session(no_load=True)}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to load session {session.session_key}: {e}'))
