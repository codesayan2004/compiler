from django.shortcuts import render
from django.http import HttpResponse
from .models import CodeSubmission
from django.conf import settings
import os
import uuid
import subprocess
from pathlib import Path
from django.template import loader
# Create your views here.

def submit_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        language = request.POST.get('language')
        input_data = request.POST.get('input_data')

        # Save the submission to the database
        submission = CodeSubmission.objects.create(
            code=code,
            language=language,
            input_data=input_data
        )
        # Process the code submission
        result = run(submission.code, submission.language, submission.input_data)
        # Update the submission with the result
        submission.result = result
        submission.status = 'completed'
        submission.save()
        # Return the result to the user
        context = {
            'submission': submission,
            'result': result,
        }
        template = loader.get_template('submit_code.html')
        return HttpResponse(template.render(context, request))
    else:
        return render(request, 'submit_code.html')
    

def run(code, language, input_data):
    project_path = Path(settings.BASE_DIR)
    directories = ["codes", "inputs", "outputs"]

    for directory in directories:
        dir_path = project_path / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
    codes_dir = project_path / "codes"
    inputs_dir = project_path / "inputs"
    outputs_dir = project_path / "outputs"
    unique = str(uuid.uuid4())

    code_file = codes_dir / f"{unique}.{language}"
    input_file = inputs_dir / f"{unique}_input.txt"
    output_file = outputs_dir / f"{unique}_output.txt"
    exe_file = codes_dir / unique

    # Save code and input to files
    code_file.write_text(code)
    input_file.write_text(input_data)

    try:
        if language == 'cpp':
            exe_path = codes_dir / unique
            compile_cmd = ['g++', str(code_file), '-o', str(exe_path)]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)

            if compile_result.returncode != 0:
                return "Compilation Error:\n" + compile_result.stderr

            try:
                with open(input_file, 'r') as f, open(output_file, 'w') as out_f:
                    exec_result = subprocess.run(
                        [str(exe_path)],
                        stdin=f,
                        stdout=out_f,
                        stderr=subprocess.PIPE,  # capture stderr separately
                        timeout=5
                    )
            except subprocess.TimeoutExpired:
                return "Time Limit Exceeded"
            except Exception as e:
                return f"Unexpected Error: {str(e)}"
        
        elif language == 'c':
            exe_path = codes_dir / unique
            compile_cmd = ['gcc', str(code_file), '-o', str(exe_path)]
            result = subprocess.run(compile_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return "Compilation Error:\n" + result.stderr
            try:
                with open(input_file, 'r') as f, open(output_file, 'w') as out_f:
                    subprocess.run(
                        [str(exe_path)], stdin=f, stdout=out_f, timeout=5
                    )
            except subprocess.TimeoutExpired:
                return "Time Limit Exceeded"

        elif language == 'py':
            try:
                with open(input_file, 'r') as f, open(output_file, 'w') as out_f:
                    subprocess.run(
                        ['python3', str(code_file)],
                        stdin=f,
                        stdout=out_f,
                        stderr=subprocess.STDOUT,
                        timeout=5  # You can change this as needed
                    )
            except subprocess.TimeoutExpired:
                return "Time Limit Exceeded"
            except Exception as e:
                return f"Runtime Error: {str(e)}"

        else:
            return "Unsupported language"
        return output_file.read_text()
    except Exception as e:
        return f"Runtime Error! : {str(e)}"
    finally:
        # Clean up temporary files
        for file in [code_file, input_file, output_file, exe_file]:
            try:
                if file.exists():
                    file.unlink()
            except Exception as e:
                print(f"Warning: Could not delete file {file}: {e}")