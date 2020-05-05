import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from libraryapp.models import Library
from libraryapp.models import model_factory
from ..connection import Connection


def get_libraries():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Library)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address
        FROM libraryapp_library l
        """)

        return db_cursor.fetchall()

@login_required
def library_form(request):
    if request.method == 'GET':
        libraries = get_libraries()
        template = 'libraries/form.html'
        context = {
            'all_libraries': libraries
        }

        return render(request, template, context)