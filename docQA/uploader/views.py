from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import UploadedDocument
from .utils import extract_content_from_excel, generate_deepseek_response


def upload_document(request):
    # <!--Default values to ensure clean state-->
    content = ""  # Default empty content
    answer = None
    error_message = None

    # Initialize form
    form = DocumentForm()

    #<!--Handle Reset Button-->
    if 'reset' in request.POST:
        # 1. Clear uploaded files in the database
        UploadedDocument.objects.all().delete()

        # 2. Clear session data (content, answer)
        request.session.flush()  # Clears session variables

        # 3. Redirect to refresh the page to a clean state
        return redirect('upload')  # Redirect ensures no cached data is shown

    # <!--File Upload -->
    elif request.method == 'POST':
        if 'file' in request.FILES:  # File upload form
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                # Save uploaded file
                document = form.save()
                file_path = document.file.path
                # Extract content and save it in session for persistence
                content = extract_content_from_excel(file_path)
                request.session['content'] = content  # Store content in session
            else:
                error_message = form.errors.as_text()

        # *Handling of Questions Asked By user
        elif 'question' in request.POST:
            question = request.POST.get('question')
            # Retrieve session content (if available)
            content = request.session.get('content', "")
            if question and content:
                # Generate AI response using DeepSeek
                answer = generate_deepseek_response(question, content)
            else:
                error_message = "No content available to process the question."

    # Retrieve content from session for display
    content = request.session.get('content', "")

    
    return render(request, 'uploader/upload.html', {
        'form': form,
        'content': content,
        'answer': answer,
        'error_message': error_message
    })


def upload_success(request):
    """ View for displaying success message """
    return render(request, 'uploader/success.html')
