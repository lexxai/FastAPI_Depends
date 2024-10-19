# FastAPI Dependency Injection: 21 Examples Using Depends() with AI Answers

## Why ?

Once I wanted to understand how Depends works in FastAPI more thoroughly to understand what's under the hood. I started communicating with the AI. The answer was a question, and I got hooked.

I decided to test it in real code and created a training project and wrote this post for it based on my questions to the AI and its answers.

Some answers were wrong, some I had already optimized a bit. But all the results shown are real and created by me personally.

The result was 21 training examples written in Python, where I checked the answers and suggestions from the AI.

Full publication:
https://lexxai.blogspot.com/2024/10/fastapi-dependency-injection-21.html

Questions:

- Prepare for use FastAPI project
- How does injection Depends work in FastAPI?
- The decision of who will run when depends on the finish route. The question is, will the yield continue?
- But the response was wrong!! We were expecting the output "Cleaning up the resource" after the error.
- So the dependency function must always be used with a try: finally?
- Okay, if depends is a class, then its instance is created once, like a singleton? How can information be saved between requests if the instance is dead after the request?
- In the redis example, should the database initialization ideally also be in the form of dependencies?
- With the asynchronous yeld for the asynchronous database initialization, is there a lot of complexity involved?

![зображення](https://github.com/user-attachments/assets/4c967767-c692-4baf-8294-a8ef5eb9a234)

## Addons:

- [ex_22.py](fastapi_learn/ex_22.py)
- [ex_23.py](fastapi_learn/ex_23.py)
- [README - ex_24](fastapi_learn/ex_24.md), [ex_24.py](fastapi_learn/ex_24.py)
- [README - ex_25](fastapi_learn/ex_25.md), [ex_25.py](fastapi_learn/ex_25.py)
