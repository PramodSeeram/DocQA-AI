from django.shortcuts import render
from .forms import DocumentForm
from .models import UploadedDocument
from .utils import extract_content_from_excel, generate_deepseek_response


def upload_document(request):
    # Initialize variables
    content = None
    answer = None
    error_message = None

    # Initialize form at the top to avoid UnboundLocalError
    form = DocumentForm()  # Default empty form for GET requests

    # Handle file upload and state persistence
    document = UploadedDocument.objects.last()  # Retrieve the last uploaded document
    if document:
        # Extract content for the last uploaded document
        file_path = document.file.path
        content = extract_content_from_excel(file_path)

    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.FILES:
            form = DocumentForm(request.POST, request.FILES)  # Reinitialize form for POST
            if form.is_valid():
                # Save the uploaded file
                document = form.save()
                file_path = document.file.path
                content = extract_content_from_excel(file_path)
            else:
                error_message = form.errors.as_text()

        # Handle question asking
        elif 'question' in request.POST:
            question = request.POST.get('question')
            if question and content:
                # Generate AI response
                answer = generate_deepseek_response(question, content)
            else:
                error_message = "No content available to process the question."

    # Render the template with updated values
    return render(request, 'uploader/upload.html', {
        'form': form,              # Form is always defined now
        'content': content,
        'answer': answer,
        'error_message': error_message
    })


def upload_success(request):
    """ View for upload success page """
    return render(request, 'uploader/success.html')
