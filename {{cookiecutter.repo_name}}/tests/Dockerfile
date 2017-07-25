FROM       base-project-image:latest
MAINTAINER your name your@email.com
ENV        REFRESHED_AT today

# set app environment to test
ENV APP_ENV test

# add all the tests
ADD ./ /var/has/{{ cookiecutter.project_name }}/tests/

# change to test directory
WORKDIR /var/has/{{ cookiecutter.project_name }}/tests

# install test packages
RUN pip install -r ./requirements/test.txt

# change back to app directory
WORKDIR /var/has/{{ cookiecutter.project_name }}

# run tests
ENTRYPOINT ["./build.py"]
CMD ["test-suite"]
