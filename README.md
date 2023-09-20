job tracker ideas/notes: 
    can let user set a goal of how many jobs or leetcode questions that they completed and have this tracked 
        -reference sec 12: bonus challenge on the Django One-to-Many Models & ModelForms lesson 
            + rather than checking against the length of the choices tuple just check against some daily goal that the user can set (store in random variable) 

search query 
    allow for users to perform a search on a website for keywords included in post content/title/tags and subforum title(or topic)/tags 
    this functionality will probably be inclusive of allowing users to filter by tags
        -for instance if we wanted to allow users to be able to click on a tag and see all related posts/subforums 

thread organization 
    have some sort of pinning or sticky subforums when it's rendered on an index page

subforum organization icebox 
    adding ux features like most recent activities/modified 

icebox 
    view subforums that a user has liked 

user roles/permissions 
    image form 
    pagination
    likes ajax call
    edited tag on subforums 

in order 
    job tracker
    pagination 
    styling 

if we implement post and comment edit 
    then maybe add another attribute on the related models that is a bool 
    then print on the screen as to whether or not its been edited 
    set a one off default for False for all preexisting rows 
    if we want to add a modified date, look back into the docs for the last modified date 
        create another attribute that stores and prints the last modified date IF that bool is True 

styling: 
    homepage 
        short 'about me' describing the web app with a couple of fonts/weights to draw the eyes down to a sign up button 
        have an overall color scheme that matches the vibes of your website 
        create some small graphics that would be reflective of how your site is used like on quizlet. maybe just some forum-type of clip art that you can throw on the homepage 
        restructure the navbar so that the links are grouped according to usage. ie login/signup on the right 
        *favicon 

job tracker notes 
    create a new job tracker model 
    create a new pdf storing model 
    create a component model for the job tracker 
        code it very similarly to posts in a subforum 
        can use ajax calls again to toggle that boolean completed field that we were talking about 
    figure out the pdf viewer 
    can use the same code for photo storage 
    need to figure out a way to limit the file type for both the photos models and pdfs 


1100