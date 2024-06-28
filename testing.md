### Manual Testing (API Endpoints)

| Method | Endpoint                           | Description                                               | Status    | Notes       |
|--------|------------------------------------|-----------------------------------------------------------|-----------|-------------|
| GET    | /                                  | Fetch all posts (homepage)                                | Pass      |             |
| GET    | /feed                              | Fetch posts from followed users                           | Pass      |             |
| GET    | /liked                             | Fetch liked posts                                         | Pass      |             |
| GET    | /channels/followed                 | Fetch followed channels                                   | Pass      |             |
| GET    | /signin                            | Sign in form                                              | Pass      |             |
| GET    | /signup                            | Sign up form                                              | Pass      |             |
| POST   | /posts/create                      | Create a new post                                         | Pass      |             |
| GET    | /posts/:id                         | Fetch a specific post by ID                               | Pass      |             |
| PUT    | /posts/:id/edit                    | Edit a specific post by ID                                | Pass      |             |
| GET    | /profiles/:id                      | Fetch a specific profile by ID                            | Pass      |             |
| POST   | /channel/create                    | Create a new channel                                      | Pass      |             |
| GET    | /channels/:title                   | Fetch a specific channel by title                         | Pass      |             |
| PUT    | /profiles/:id/edit/username        | Edit username of a specific profile by ID                 | Pass      |             |
| PUT    | /profiles/:id/edit/password        | Edit password of a specific profile by ID                 | Pass      |             |
| PUT    | /profiles/:id/edit                 | Edit a specific profile by ID                             | Pass      |             |
| PUT    | /channels/:title/edit              | Edit a specific channel by title                          | Pass      |             |
| GET    | /*                                 | Catch-all for undefined routes (Page not found)           | Pass      |             |
