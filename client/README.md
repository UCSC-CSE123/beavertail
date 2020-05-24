# client

These files form the client for beavertail. They are served statically with an
Nginx container, which is also configured to serve the SQLite database that
stores population density information that is written to by the server.

If, for some reason, you wanted to run this without Docker, you could serve the
files in this directory statically (e.g., `python -m http.server`) after
symlinking the database file to this directory. This note is really just here
for propriety.
