FROM node:22-alpine

WORKDIR /app

ARG NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
ENV NEXT_PUBLIC_API_BASE_URL=${NEXT_PUBLIC_API_BASE_URL}

COPY package.json package-lock.json* /app/
RUN npm install

COPY . /app
RUN npm run build

CMD ["npm", "run", "start"]
