
<h1 align="center">
  <br>
  <img src="./static/leo.png" alt="Leo" width="200">
  <br>
  Leo
  <br>
</h1>

<h4 align="center">A teaching assistant of <a href="https://spartacodingclub.kr" target="_blank">Sparta Coding Club</a>.</h4>

<p align="center">
  <a href="https://travis-ci.org/yeojin-dev/leo"><img src="https://travis-ci.org/yeojin-dev/leo.svg?branch=master"></a>
  <a href="https://coveralls.io/github/yeojin-dev/leo?branch=master">
      <img src="https://coveralls.io/repos/github/yeojin-dev/leo/badge.svg?branch=master">
  </a>
</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#license">License</a>
</p>

## Key Features

* 숙제 제출 기능
  * HTML 파일 제출 이후 인터넷으로 확인할 수 있는 링크 제공

## How To Use

### Requirements

* python 3.8
* mongodb 4.2
* .env.template 파일을 활용해 .env 파일을 생성

### Run in local env.

파이썬 가상환경에서 아래 스크립트 사용

```bash
$ python app.py
```

### Run a Docker container

도커 이미지 빌드는 아래 스크립트 사용

```bash
$ docker build --tag leo:latest --rm .
```

빌드 이후 컨테이너 실행

```bash
$ docker run -d -p 5000:5000 leo:latest
```

## License

MIT
