<h1>Django Chess Game</h1>

A 2-player chess game built with Django and AJAX.
The app supports user authentication, real-time gameplay, game room management, and match history tracking.

 <h2>Features</h2>
<h4>Authentication & Registration</h4>
<ul>
<li>Users can log in with email, username, and password.</li>

<li>New users must create an account before playing.</li>
</ul>
<h4>Main Lobby</h4>
<ul>
<li>Create Room – Create a game room. The creator becomes the white player and sets the time per player.</li>

<li>Join Room – Browse available rooms and join as the black player.</li>

<li>History – View past matches, including opponents and results (white, black, or draw).</li>
</ul>
<h4>Game Mechanics</h4>
<u>
<li>Real-time move updates via AJAX.</li>

<li>Pieces highlight possible moves.</li>

<li>Displays the current turn, check status, and winner.</li>

<li>At the end of the game, a result message appears with a Rematch button.</li>
</ul>
<h4> Technologies Used</h4>
<ul>
<li>Backend: Python 3, Django</li>

<li>Real-Time Communication: AJAX</li>

<li>Database: SQLite (Django default)</li>

<li>Frontend: HTML, CSS, JavaScript</li>
</ul>
<h3>Running Locally</h3>

<h4>Clone the repository:</h4>

<pre>git clone [https://github.com/<username>/repo.git](https://github.com/ioanavlad3/chess-django)
</pre>


<h4>Create and activate a virtual environment:</h4>

<pre>python -m venv env 
source env/bin/activate   # Linux/Mac
env\Scripts\activate      # Windows  </pre>


<h4>Install dependencies:</h4>

<pre>pip install -r requirements.txt</pre>


<h4>Apply migrations:</h4>

<pre>python manage.py migrate</pre>


<h4>Run the development server:</h4>

<pre>python manage.py runserver</pre>


<h4>Open the app in your browser:</h4>
<pre>http://localhost:8000</pre>
