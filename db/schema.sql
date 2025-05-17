/**
 * Database schema for cinema seat reservation app
 */
CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    genre_id INTEGER REFERENCES genres(id),
    duration INTEGER NOT NULL,
    release_date DATE NOT NULL,
    description TEXT,
    poster_url VARCHAR(255)
);

CREATE TABLE halls (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    rows INTEGER NOT NULL,
    columns INTEGER NOT NULL
);

CREATE TABLE showtimes (
    id SERIAL PRIMARY KEY,
    movie_id INTEGER REFERENCES movies(id),
    hall_id INTEGER REFERENCES halls(id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('admin', 'user')) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    showtime_id INTEGER REFERENCES showtimes(id),
    seat_number VARCHAR(10) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('pending', 'confirmed', 'canceled')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial genres
INSERT INTO genres (name) VALUES
('Action'), ('Comedy'), ('Drama'), ('Sci-Fi'), ('Horror'),
('Romance'), ('Adventure'), ('Thriller'), ('Fantasy'), ('Animation'),
('Documentary'), ('Crime'), ('Mystery'), ('Family'), ('Historical');