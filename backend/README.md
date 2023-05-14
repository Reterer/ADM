# Backend

используется fastapi

---

## Как запустисть dev-сервер и вообще что-то.

### Создать виртуальное окружение и установить туда нужные библиотекки 
```bash
cd app
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

### Запуск dev-сервера
```
uvicorn main:app --reload
```
---
