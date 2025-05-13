# 🚀 Projeto Docker com Docker Compose

Este projeto utiliza Docker e Docker Compose para orquestrar os serviços de forma simples e eficiente. Ideal para desenvolvimento, testes e deploy local de aplicações baseadas em múltiplos containers.

---

## 📁 Estrutura do Projeto

```
.
├── docker-compose.yml       # Definição dos serviços
├── Dockerfile               # (opcional) Imagem customizada do serviço
├── .env                     # (opcional) Variáveis de ambiente
└── README.md                # Este arquivo
```

---

## ▶️ Subindo os serviços

```bash
docker compose up -d
```

> Sobe os containers em modo "detached" (em segundo plano).

---

## ♻️ Recriando os containers (com rebuild)

```bash
docker compose up -d --build
```

> Reconstrói as imagens e reinicia os serviços.

---

## 👏 Parando e removendo os containers

```bash
docker compose down
```

Para remover volumes e imagens juntos:

```bash
docker compose down --volumes --rmi all
```

---

## 🔀 Reiniciando os serviços

```bash
docker compose restart
```

---

## 📜 Logs dos serviços

```bash
docker compose logs -f
```

---

## 🧠 Status dos containers

```bash
docker compose ps
```

---

## 🧹 Limpeza total de redes, volumes e containers

> ⚠️ Use com cuidado! Remove **tudo** que não estiver em uso.

```bash
docker system prune -a --volumes
```

---

## ❌ Erro comum e solução

### Erro:

```
! Network api_python_default  Resource is still in use
```

### Solução:

```bash
docker compose down
docker network rm api_python_default
```

Ou:

```bash
docker stop $(docker ps -q)
docker rm $(docker ps -aq)
docker network prune -f
```

---

## ✅ Verificando redes e containers

```bash
docker ps -a
docker network ls
docker network inspect NOME_DA_REDE
```

---

## 📦 Dica: Remover orfãos (containers não usados)

```bash
docker compose down --remove-orphans
```

---

## 🗪 Testando interações

Para acessar o terminal de um container:

```bash
docker exec -it nome_do_container bash
```

---

## ✨ Pronto!

Agora você tem um ambiente Docker organizado e com comandos prontos para qualquer necessidade!
