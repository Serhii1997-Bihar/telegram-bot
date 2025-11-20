def server(bot, call):
    notate = (
        "<code>|nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &</code>\n"
        "<code>|ps aux | grep manage.py runserver</code>\n"
        "<code>|tail -n 20 server.log</code>\n"
        "<code>|pkill -f \"manage.py runserver\"</code>\n"
        "<code>|scp -r C:\PyCharm\work_projects\18.03.2025\pricesua_project\pricesua_project root@116.203.238.17:/root/price/</code>\n"
        "<code>|kill 2554458</code>\n"
        "<code>|pip install -r requirements.txt</code>\n"
        "<code>|scp -r user@host:/remote/folder ./local</code>\n"
        "<code>|apt update && apt install -y postgresql ...</code>\n"
        "<code>|sudo -u postgres psql</code>")
    bot.send_message(call.message.chat.id, f"<pre>{notate}</pre>", parse_mode='HTML')

def docker(bot, call):
    commands = (
        "<code>|docker build -t myimage .</code>\n"
        "<code>|docker run -d -p 8000:8000 myimage</code>\n"
        "<code>|docker-compose up --build -d</code>\n"
        "<code>|docker ps</code>\n"
        "<code>|docker stop e34r5t4y5</code>\n"
        "<code>|docker ps -a</code>\n"
        "<code>|docker rm &lt;container_id&gt;</code>\n"
        "<code>|docker logs &lt;container_id&gt;</code>\n"
        "<code>|docker exec -it &lt;container_id&gt; /bin/bash</code>\n"
        "<code>|docker-compose up -d</code>\n"
        "<code>|docker-compose down</code>\n\n"
        "<code>|sudo apt update</code>\n"
        "<code>|sudo apt upgrade -y</code>\n"
        "<code>|sudo apt install apt-transport-https ca-certificates curl software-properties-common -y</code>\n"
        "<code>|curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg</code>\n"
        "<code>|echo \"deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null</code>\n"
        "<code>|sudo apt update</code>\n"
        "<code>|sudo apt install docker-ce docker-ce-cli containerd.io -y</code>\n"
        "<code>|sudo systemctl status docker</code>\n"
        "<code>|sudo docker run hello-world</code>\n"
    )

    docker = (
        "<pre><code class=\"language-dockerfile\">"
        "FROM python:3.11.4\n"
        "WORKDIR /app\n"
        "COPY . /app\n"
        "RUN pip install --no-cache-dir -r requirements.txt\n"
        "EXPOSE 8001\n"
        "CMD [\"python\", \"manage.py\", \"runserver\", \"0.0.0.0:8001\"]"
        "</code></pre>\n"

        "<pre><code class=\"language-yaml\">"
        "version: '3.8'\n"
        "features:\n"
        "\n"
        "  web:\n"
        "    build: .\n"
        "    restart: always\n"
        "    ports:\n"
        "      - \"8001:8001\"\n"
        "    volumes:\n"
        "      - .:/app\n"
        "    command: python manage.py runserver 0.0.0.0:8001\n"
        "    depends_on:\n"
        "      - db\n"
        "\n"
        "  bot:\n"
        "    build: .\n"
        "    restart: always\n"
        "    command: python modules/bot.py\n"
        "    depends_on:\n"
        "      - db\n"
        "\n"
        "  db:\n"
        "    image: postgres:16\n"
        "    restart: always\n"
        "    environment:\n"
        "      POSTGRES_DB: working_db\n"
        "      POSTGRES_USER: postgres\n"
        "      POSTGRES_PASSWORD: Hardwell1997\n"
        "    volumes:\n"
        "      - postgres_data:/var/lib/postgresql/data\n"
        "\n"
        "volumes:\n"
        "  postgres_data:"
        "</code></pre>")


    bot.send_message(call.message.chat.id, f"<pre>{commands}</pre>", parse_mode='HTML')
    bot.send_message(call.message.chat.id, docker, parse_mode='HTML')

def mongodb(bot, call):
    commands = (
        "<code>|sudo apt install -y mongodb</code>\n"
        "<code>|sudo systemctl start mongodb</code>\n"
        "<code>|sudo systemctl status mongodb</code>\n"
        "<code>|sudo systemctl enable mongodb</code>\n"
        "<code>|mongo</code>\n"
        "<code>|mongo --host 127.0.0.1 --port 27017</code>\n"
        "<code>|mongodump --db=test --out=/backup/test</code>\n"
        "<code>|mongorestore --db=test /backup/test</code>\n"
        "<code>|sudo service mongod restart</code>\n"
        "<code>|sudo service mongod stop</code>\n"
        "<code>|sudo service mongod start</code>\n"
        "<code>|use mydatabase</code>\n"
        "<code>|db.mycollection.insertOne({name: \"Serhii\", age: 28})</code>\n"
        "<code>|db.mycollection.find()</code>\n"
        "<code>|db.mycollection.updateOne({name: \"Serhii\"}, {$set: {age: 29}})</code>\n"
        "<code>|db.mycollection.deleteOne({name: \"Serhii\"})</code>\n"
        "<code>|show dbs</code>\n"
        "<code>|show collections</code>\n")
    bot.send_message(call.message.chat.id, f"<pre>{commands}</pre>", parse_mode='HTML')

def git(bot, call):
    commands = (
        "<code>|git init</code>\n"
        "<code>|git clone https://github.com/user/repo.git</code>\n"
        "<code>|git status</code>\n"
        "<code>|git add .</code>\n"
        "<code>|git commit -m \"Initial commit\"</code>\n"
        "<code>|git push origin main</code>\n"
        "<code>|git pull origin main</code>\n"
        "<code>|git branch</code>\n"
        "<code>|git checkout -b new-branch</code>\n"
        "<code>|git checkout main</code>\n"
        "<code>|git merge new-branch</code>\n"
        "<code>|git log</code>\n"
        "<code>|git remote -v</code>\n"
        "<code>|git stash</code>\n"
        "<code>|git stash apply</code>\n"
        "<code>|git reset --hard</code>\n"
        "<code>|git config --global user.name \"Your Name\"</code>\n"
        "<code>|git config --global user.email \"your.email@example.com\"</code>\n"
    )
    bot.send_message(call.message.chat.id, f"<pre>{commands}</pre>", parse_mode='HTML')

def firewall(bot, call):
    notate = (
        "<code>|ufw status</code>\n"
        "<code>|ufw enable</code>\n"
        "<code>|ufw disable</code>\n"
        "<code>|ufw allow 8000/tcp</code>\n"
        "<code>|ufw deny 22</code>\n"
        "<code>|ufw delete allow 8000/tcp</code>\n"
        "<code>|iptables -L -v -n</code>\n"
        "<code>|iptables -A INPUT -p tcp --dport 80 -j ACCEPT</code>\n"
        "<code>|iptables -D INPUT -p tcp --dport 80 -j ACCEPT</code>\n"
        "<code>|systemctl restart ufw</code>\n"
        "<code>|firewall-cmd --list-all</code>\n")
    bot.send_message(call.message.chat.id, f"<pre>{notate}</pre>", parse_mode='HTML')

def nginx(bot, call):
    notate = (
        "<code>worker_processes auto;</code> — автоматичний вибір кількості воркерів\n"
        "<code>events { worker_connections 1024; }</code> — налаштування подій (максимум з’єднань)\n"
        "<code>http {</code> — початок HTTP-блоку\n"
        "    <code>server {</code> — початок конфігурації сервера\n"
        "        <code>listen 80;</code> — слухати порт 80 (HTTP)\n"
        "        <code>server_name example.com www.example.com;</code> — домени\n"
        "        <code>location / {</code> — налаштування кореневого шляху\n"
        "            <code>proxy_pass http://127.0.0.1:8000;</code> — проксі до Django (або іншого)\n"
        "            <code>proxy_set_header Host $host;</code> — передача хосту\n"
        "            <code>proxy_set_header X-Real-IP $remote_addr;</code> — IP клієнта\n"
        "            <code>proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;</code>\n"
        "            <code>proxy_set_header X-Forwarded-Proto $scheme;</code>\n"
        "        <code>}</code>\n"
        "    <code>}</code>\n"
        "<code>}</code> — кінець HTTP-блоку\n")
    bot.send_message(call.message.chat.id, f"<pre>{notate}</pre>", parse_mode='HTML')