**github-flask-client** 

### Welcome to github client!

This small application interacts with github and provides some statistics about users and repositories.

This application exposes two endpoints:

1. active/{user}
2. downwards/{owner}/{repository}

The first endpoint shows, how active the user is.
The endpoint returns JSON response with boolean <code>isActive</code> field.
If the user has pushed the code to any repository in the last 24 hours, the field will have the value true or false, depending on the results of user's activity.

{user} parameter denotes username of the person on github.
{owner} is the same as the parameter, but in the second endpoint it means, that the user owns the repository.
{repository} is the name of the repository, it could be found at user's page on github.

The second endpoint shows, whether the amount of the code has been reduced in the repository.
The endpoint returns JSON response with boolean field <code>downwards</code>.
If there were more additions, than deletions in the last 7 days, then this field will be set to true.
In other scenario this field will be set to false.

!This app is able to query only PUBLIC github repositories. The private repositories and events will not be taken into account!

In order to call the endpoints, you could use any clients for queries (like curl etc) or browser.
The example url: <code>http://localhost:5000/active/username</code>

In case of unexpected behavior or errors the json with single 'error_message' field is returned.
This field contains error message in text format.

Enjoy!

### running app with docker

to run app with docker, you have to execute the following commands:

- install docker
- go to the project directory
- run command <code>docker build -t githubclient:latest .</code>
- run command <code>docker run -p 5000:5000 githubclient</code> 


If you run the app from the console, you should see the message:
<code>Running on http://0.0.0.0:5000/</code>

But actually your application will run on <code>http://localhost:5000</code>.
