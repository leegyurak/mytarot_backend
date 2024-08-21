 
<h1 align="center">
  <br>
  <a href="https://mytarot.devgyurak.com/"><img src="https://imagedelivery.net/R9FsTLXBX6-6fZLUqzGBBg/dfc4a526-b8e2-4064-aa4d-f97d20c2ae00/public" alt="상징 타로 찾기" width="200"></a>
  <br>
  상징 타로 찾기 (BE)
  <br>
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql" alt="MySQL">
  <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker" alt="Docker">
  <img src="https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions" alt="Github Action">
</p>

![스크린샷](https://github.com/user-attachments/assets/db846a5a-9600-4454-94d8-4f174e20755d)

## 주요 기능

* 생일 입력
  - 특정 날자를 FastAPI의 APIRouter로 받습니다
* 해당하는 타로 카드 찾기
  - 생일을 바탕으로 한 공식 결과를 SQLAlchemy Entity에 조회해 해당 하는 타로카드를 가져옵니다.
* 프롬프팅
  - Claude(Anthropic) API에 타로의 이름, 해설, 좋은 뜻들 및 나쁜 뜻들을 프롬프팅하여 카드에 대한 해설을 가져옵니다.

## 환경 세팅 및 실행

- [Git](https://git-scm.com), [Python](https://www.python.org/downloads/), [MySQL](https://www.mysql.com/), 그리고 [Poetry](https://python-poetry.org/)가 필요해요!

```bash
# Clone this repository
$ git clone https://github.com/leegyurak/joatss_backend

# Go into the repository
$ cd mytarot_backend

# Enter vitual environment
$ poetry shell

# Install dependencies
$ poetry install

# Add Environment Variable
$ CLAUDE_API_KEY=${add your API key}
$ MYSQL_HOST=${add your MySQL host}
$ MYSQL_PORT=${add your MySQL port}
$ MYSQL_USER=${add your MySQL user}
$ MYSQL_PASSWORD=${add your MySQL password}
$ MYSQL_DATABASE=${add your MySQL database}

# Run migrate
$ alembic upgrade head

# Run server
$ python main.py
```

> 도커 파일을 빌드해도 실행 가능합니다!

## 사용하기

- [상징 타로 찾기 접속](https://mytarot.devgyurak.com/) 

## License

MIT

---

[issues-badge]: https://img.shields.io/github/issues/mkosir/react-parallax-tilt
[issues-url]: https://github.com/leegyurak/joatss_backend/issues
