FROM node:18-alpine

WORKDIR /usr/src/app

COPY package.json package-lock.json ./
RUN npm install

# COPY . .  # don't need to do this, if mounting files from docker compose

CMD ["npm", "start"]
