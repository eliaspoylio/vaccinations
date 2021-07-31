FROM node:lts-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

#RUN npm install -g http-server

#RUN npm run build

CMD ["npm", "run", "serve"]
#CMD [ "http-server", "-p 80", "dist" ]