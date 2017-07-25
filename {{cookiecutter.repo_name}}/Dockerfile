FROM       python:3.5-alpine
MAINTAINER {{ cookiecutter.author_name }} {{ cookiecutter.email }}
ENV        REFRESHED_AT {{ cookiecutter.now }}

# Expose ports
EXPOSE 8000

# Make application dir
RUN mkdir -p /var/{{ cookiecutter.repo_name }}

# Add initial requirements and install before adding code to allow for better caching
ADD ./requirements.txt /var/{{ cookiecutter.repo_name }}/requirements.txt
WORKDIR /var/{{ cookiecutter.repo_name }}
RUN pip install -r ./requirements.txt

# add app code
ADD ./ /var/{{ cookiecutter.repo_name }}/

# run app
ENTRYPOINT ["gunicorn"]

# add for trouble shooting "--preload", "--log-file=-"
CMD ["-b", "0.0.0.0:8000", "--log-file=-", "--workers=5", "wsgi:application"]
