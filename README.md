<h1 align="center">Hello-Fresh-Code-Challenge-Backend</h1>

<p align="center">Backend for a menu planning service that allows to 
manage weekly menu and associated recipies.</p>

## Links

- [Repo](https://github.com/mmoize/Hello-Fresh-Code-Challenge "<Hello-Fresh-Code-Challenge> Repo")


## Screenshots

![Home Page](/screenshots/1.png "Home Page")

![](/screenshots/Hello-fresh-code-Screenshot.png)

![](/screenshots/Hello-fresh-code-Screenshot-2.png)

## Available Commands

In the project directory, you can run:

### `Python manage.py makemigrations" : "Python manage.py migrate"`,

This Backend service is built using `Python Django` thus this command Runs the service in Development mode. Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view it in the browser. 
You also need to  open up Postman for testing the rest api.
Inorder to make requests to the backend you will have to signup with an email and password and use the returned JWT Token for all requests to the service.

### `"npm run build": "react-scripts build"`,

Builds the app for production to the `build` folder. It correctly bundles React in production mode and optimizes the build for the best performance. The build is minified and the filenames include the hashes. Your app will be ready to deploy!

### `"npm run test": "react-scripts test"`,

Launches the test runner in the interactive watch mode.

### `"npm run dev": "concurrently "nodemon server" "npm run start"`,

For running the server and app together I am using concurrently this helps a lot in the MERN application as it runs both the server (client and server) concurrently. So you can work on them both together.

### `"serve": "node server"`

For running the server file on you can use this command.

### `npm run serve`

## Built With

- Python Django
- Rest Frame Work
- Postgres
- Containerized with docker


## Future Updates

- [ ] Reliable Storage

## Author

**Moise Murhi**

