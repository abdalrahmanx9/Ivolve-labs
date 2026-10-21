FROM node:22-alpine

WORKDIR /app

COPY package.json ./

RUN npm install --omit=dev \
    && npm cache clean --force \
    && rm -rf /usr/local/lib/node_modules /usr/local/bin/npm /usr/local/bin/npx

COPY app.js ./

EXPOSE 3000

CMD ["node", "app.js"]
