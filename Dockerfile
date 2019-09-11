FROM codeif/pipenv-example

COPY . /app

WORKDIR /app/example

ENV TZ=Asia/Shanghai PYTHONUNBUFFERED=1
ENV FLASK_ENV=development FLASK_APP=demo
ENV PIPENV_PYPI_MIRROR=https://pypi.tuna.tsinghua.edu.cn/simple

RUN pipenv sync

EXPOSE 5000

CMD ["pipenv", "run", "flask", "run", "-h", "0.0.0.0"]
