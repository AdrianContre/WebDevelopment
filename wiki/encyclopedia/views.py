from django.shortcuts import render, redirect

from . import util

from django.http import Http404
from markdown2 import Markdown
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import os
from random import choice

class NewForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 10, "cols": 40}),
        label="Content")

class EditForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"readonly": "readonly"}))
    content = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 10, "cols": 40}),
        label="Content")






def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request,entry):
    found = False
    entries = util.list_entries()
    for item in entries:
        if item == entry:
            found = True
            break
    if found == False:
        raise Http404("No entry found")
    content = util.get_entry(entry)
    return render(request,"encyclopedia/wiki.html", {
        "title": entry, "content": Markdown().convert(content)
    })

def search(request):
    query = request.GET.get("q","")
    content = util.get_entry(query)
    if query != None and content != None:
        return render(request,"encyclopedia/wiki.html", {
            "title": query, "content": Markdown().convert(content)
        })
    elif query != None:
        all_entries = util.list_entries()
        substrings = []
        for item in all_entries:
            if query.lower() in item.lower():
                substrings.append(item)
        if len(substrings) == 0:
            substrings = all_entries
        return render(request,"encyclopedia/search.html", {
            "list_entries": substrings
        })

def newPage(request):
    if request.method == "GET":
        return render(request,"encyclopedia/newPage.html", {
            "form": NewForm()
        })
    elif request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            title_entry = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            check = util.get_entry(title_entry)
            all_entries = util.list_entries()
            check2 = False
            for item in all_entries:
                if item.lower() == title_entry or item.lower() == title_entry.lower() or item == title_entry.lower():
                    check2 = True
                    break
            if check != None or check2 == True:
                return render(request,"encyclopedia/error.html")
            else:
                file_path = os.path.join('entries', f'{title_entry}.md')
                with open(file_path, 'w') as file:
                    file.write(content)
                return redirect("wiki",title_entry)
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/newPage.html", {
                "form": form
            })

def edit(request,title):
    if request.method == "GET":
        form = EditForm(initial={"title": title, "content": util.get_entry(title)})
        return render(request, "encyclopedia/edit.html", {"form": form})
    elif request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            newContent = form.cleaned_data["content"]
            util.save_entry(title,newContent)
            return redirect("wiki",title)
        else:
            form = EditForm(initial={"title": title, "content": util.get_entry(title)})
            return render(request, "encyclopedia/edit.html", {
                "form": form
            })

def random(request):
    all_titles = util.list_entries()
    title = choice(all_titles)
    return redirect('wiki',title)


def customhandler404(request):
    response = render(request, '404.html',)
    response.status_code = 404
    return response









