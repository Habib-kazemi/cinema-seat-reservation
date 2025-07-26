--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS '';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cinema; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cinema (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    address character varying(255) NOT NULL
);


ALTER TABLE public.cinema OWNER TO postgres;

--
-- Name: cinema_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cinema_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cinema_id_seq OWNER TO postgres;

--
-- Name: cinema_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cinema_id_seq OWNED BY public.cinema.id;


--
-- Name: genre; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.genre (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.genre OWNER TO postgres;

--
-- Name: genre_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.genre_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.genre_id_seq OWNER TO postgres;

--
-- Name: genre_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.genre_id_seq OWNED BY public.genre.id;


--
-- Name: hall; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.hall (
    id integer NOT NULL,
    cinema_id integer NOT NULL,
    name character varying(100) NOT NULL,
    rows integer NOT NULL,
    columns integer NOT NULL
);


ALTER TABLE public.hall OWNER TO postgres;

--
-- Name: hall_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.hall_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.hall_id_seq OWNER TO postgres;

--
-- Name: hall_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.hall_id_seq OWNED BY public.hall.id;


--
-- Name: movie; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movie (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    genre_id integer,
    duration integer NOT NULL,
    release_date date NOT NULL,
    description text,
    poster_url character varying(255)
);


ALTER TABLE public.movie OWNER TO postgres;

--
-- Name: movie_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.movie_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.movie_id_seq OWNER TO postgres;

--
-- Name: movie_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.movie_id_seq OWNED BY public.movie.id;


--
-- Name: reservation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reservation (
    id integer NOT NULL,
    user_id integer,
    showtime_id integer,
    seat_number character varying(10) NOT NULL,
    price numeric(10,2) NOT NULL,
    status character varying(20) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT reservation_status_check CHECK (((status)::text = ANY ((ARRAY['PENDING'::character varying, 'CONFIRMED'::character varying, 'CANCELED'::character varying])::text[])))
);


ALTER TABLE public.reservation OWNER TO postgres;

--
-- Name: reservation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reservation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reservation_id_seq OWNER TO postgres;

--
-- Name: reservation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reservation_id_seq OWNED BY public.reservation.id;


--
-- Name: showtime; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.showtime (
    id integer NOT NULL,
    movie_id integer,
    hall_id integer,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone NOT NULL,
    price numeric(10,2) NOT NULL
);


ALTER TABLE public.showtime OWNER TO postgres;

--
-- Name: showtime_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.showtime_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.showtime_id_seq OWNER TO postgres;

--
-- Name: showtime_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.showtime_id_seq OWNED BY public.showtime.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role character varying(20) NOT NULL,
    full_name character varying(255) NOT NULL,
    phone_number character varying(20),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT users_role_check CHECK (((role)::text = ANY ((ARRAY['ADMIN'::character varying, 'USER'::character varying])::text[])))
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: cinema id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cinema ALTER COLUMN id SET DEFAULT nextval('public.cinema_id_seq'::regclass);


--
-- Name: genre id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.genre ALTER COLUMN id SET DEFAULT nextval('public.genre_id_seq'::regclass);


--
-- Name: hall id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hall ALTER COLUMN id SET DEFAULT nextval('public.hall_id_seq'::regclass);


--
-- Name: movie id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movie ALTER COLUMN id SET DEFAULT nextval('public.movie_id_seq'::regclass);


--
-- Name: reservation id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservation ALTER COLUMN id SET DEFAULT nextval('public.reservation_id_seq'::regclass);


--
-- Name: showtime id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.showtime ALTER COLUMN id SET DEFAULT nextval('public.showtime_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: cinema; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cinema (id, name, address) FROM stdin;
2	Cinema B	456 Elm St
38	Cinema C	Test Address
1	Cinema A	122 Main St
\.


--
-- Data for Name: genre; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.genre (id, name) FROM stdin;
1	Action
2	Comedy
3	Drama
4	Sci-Fi
5	Horror
6	Romance
7	Adventure
8	Thriller
9	Fantasy
10	Animation
11	Documentary
12	Crime
13	Mystery
14	Family
15	Historical
\.


--
-- Data for Name: hall; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.hall (id, cinema_id, name, rows, columns) FROM stdin;
2	2	Hall B1	8	12
56	2	Hall C	10	30
1	1	Hall A	10	20
57	38	Hall A	15	30
\.


--
-- Data for Name: movie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.movie (id, title, genre_id, duration, release_date, description, poster_url) FROM stdin;
2	Comedy Movie	2	90	2025-02-01	\N	\N
28	Action Movie	1	135	2025-07-16	string	string
\.


--
-- Data for Name: reservation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reservation (id, user_id, showtime_id, seat_number, price, status, created_at) FROM stdin;
86	7	42	A5	12.00	CONFIRMED	2025-07-19 21:05:22.308933
87	7	42	A6	12.00	CONFIRMED	2025-07-19 21:05:28.012624
88	7	42	A7	12.00	CONFIRMED	2025-07-19 21:05:32.988389
89	7	42	B7	12.00	CONFIRMED	2025-07-19 21:05:42.122763
90	7	42	B5	12.00	CONFIRMED	2025-07-19 21:05:51.737724
91	10	43	A3	9.50	CONFIRMED	2025-07-19 21:13:30.002721
92	10	43	A4	9.50	CONFIRMED	2025-07-19 21:13:38.37937
93	10	43	A5	9.50	CONFIRMED	2025-07-19 21:13:42.83336
94	10	43	A6	9.50	CONFIRMED	2025-07-19 21:13:47.10916
95	10	43	A7	9.50	CONFIRMED	2025-07-19 21:13:51.528449
96	10	43	A8	9.50	CONFIRMED	2025-07-19 21:14:00.761095
97	10	43	B8	9.50	CONFIRMED	2025-07-19 21:14:06.240756
98	10	43	B7	9.50	CONFIRMED	2025-07-19 21:14:12.703551
99	10	43	B6	9.50	CONFIRMED	2025-07-19 21:14:17.208638
100	10	43	B5	9.50	CONFIRMED	2025-07-19 21:14:22.272643
101	10	43	B4	9.50	CONFIRMED	2025-07-19 21:14:26.678708
102	10	43	B3	9.50	CONFIRMED	2025-07-19 21:14:31.327141
80	5	41	A5	14.50	CONFIRMED	2025-07-17 22:33:47.836287
81	5	41	A6	14.50	CONFIRMED	2025-07-17 22:34:54.466829
82	5	41	A7	14.50	CONFIRMED	2025-07-17 22:34:59.062185
83	5	41	A8	14.50	CONFIRMED	2025-07-17 22:35:03.399235
103	10	44	B3	11.50	CONFIRMED	2025-07-19 21:21:38.57457
104	10	44	B4	11.50	CONFIRMED	2025-07-19 21:21:44.559406
105	10	44	B5	11.50	CONFIRMED	2025-07-19 21:21:50.451004
106	10	44	C5	11.50	CONFIRMED	2025-07-19 21:21:54.492092
107	10	44	C4	11.50	CONFIRMED	2025-07-19 21:22:01.460831
108	10	44	C3	11.50	CONFIRMED	2025-07-19 21:22:05.620418
109	10	45	C3	11.50	CONFIRMED	2025-07-19 21:22:13.994167
110	10	45	C4	11.50	CONFIRMED	2025-07-19 21:22:19.25762
111	10	45	C6	11.50	CONFIRMED	2025-07-19 21:22:24.006517
112	10	45	C5	11.50	CONFIRMED	2025-07-19 21:22:30.826988
113	10	45	D5	11.50	CONFIRMED	2025-07-19 21:22:41.22608
114	10	45	D4	11.50	CONFIRMED	2025-07-19 21:22:45.541803
115	10	45	D3	11.50	CONFIRMED	2025-07-19 21:22:49.930202
116	10	45	D6	11.50	CONFIRMED	2025-07-19 21:22:55.780828
117	10	45	D7	11.50	CANCELED	2025-07-19 21:23:00.699311
\.


--
-- Data for Name: showtime; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.showtime (id, movie_id, hall_id, start_time, end_time, price) FROM stdin;
41	2	2	2025-07-16 23:34:58.008	2025-07-17 02:04:58.008	14.50
42	2	1	2025-07-17 18:22:48.927	2025-07-17 20:22:48.927	12.00
43	28	56	2025-07-19 21:10:36.33	2025-07-19 22:40:36.33	9.50
44	28	57	2025-07-19 21:10:36.33	2025-07-19 23:15:36.33	11.50
45	2	57	2025-07-19 23:15:36.33	2025-07-20 01:15:36.33	11.50
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, email, password_hash, role, full_name, phone_number, created_at) FROM stdin;
1	admin@example.com	$2b$12$dQkSlMwcTbiV0JhUoDgXyuT/Mz/TqUbbNBfOF8l0RevAUiK4hEuZW	ADMIN	Admin User	1234567890	2025-07-08 22:33:55.142358
2	user@example.com	$2b$12$RyTX2FTyOSxegrI0DsPrwu7ZjEXBp1wO9Gl3cFfCkwqtxlER2ZWqy	USER	Normal User	0987654321	2025-07-08 22:33:55.142358
5	testuser3@example.com	$2b$12$OiAPkSwKlRhf5IKgJTpx6uwG/G8.tHEnCuDnMQSpOqTgXR2htoXay	USER	test user3	string	2025-07-16 19:26:57.03348
7	testuser@example.com	$2b$12$nZzVNWyDc5K0zBiixCyhqeC/0yicwBm.cMOlstyTpwxkw33OA8ffG	USER	test user1	string	2025-07-17 17:17:45.251556
8	testuser2@example.com	$2b$12$8AAs0mo/cEsJIFX7cWzYHOhbHOLZkRxRgrPeGmgqq5yUElFat1aei	USER	test user2	string	2025-07-17 17:20:40.022383
10	testadmin3@example.com	$2b$12$HpEY5GCyVhaJkOCEN4NQnecbBinX6bI5re1EspENd1Z2KIHWa7O/i	ADMIN	test admin3	string	2025-07-17 17:36:39.2995
\.


--
-- Name: cinema_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cinema_id_seq', 38, true);


--
-- Name: genre_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.genre_id_seq', 15, true);


--
-- Name: hall_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.hall_id_seq', 57, true);


--
-- Name: movie_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.movie_id_seq', 28, true);


--
-- Name: reservation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reservation_id_seq', 117, true);


--
-- Name: showtime_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.showtime_id_seq', 45, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 10, true);


--
-- Name: cinema cinema_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cinema
    ADD CONSTRAINT cinema_pkey PRIMARY KEY (id);


--
-- Name: genre genre_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.genre
    ADD CONSTRAINT genre_pkey PRIMARY KEY (id);


--
-- Name: hall hall_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hall
    ADD CONSTRAINT hall_pkey PRIMARY KEY (id);


--
-- Name: movie movie_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movie
    ADD CONSTRAINT movie_pkey PRIMARY KEY (id);


--
-- Name: reservation reservation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservation
    ADD CONSTRAINT reservation_pkey PRIMARY KEY (id);


--
-- Name: showtime showtime_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.showtime
    ADD CONSTRAINT showtime_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: hall hall_cinema_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hall
    ADD CONSTRAINT hall_cinema_id_fkey FOREIGN KEY (cinema_id) REFERENCES public.cinema(id);


--
-- Name: movie movie_genre_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movie
    ADD CONSTRAINT movie_genre_id_fkey FOREIGN KEY (genre_id) REFERENCES public.genre(id);


--
-- Name: reservation reservation_showtime_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservation
    ADD CONSTRAINT reservation_showtime_id_fkey FOREIGN KEY (showtime_id) REFERENCES public.showtime(id);


--
-- Name: reservation reservation_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservation
    ADD CONSTRAINT reservation_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: showtime showtime_hall_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.showtime
    ADD CONSTRAINT showtime_hall_id_fkey FOREIGN KEY (hall_id) REFERENCES public.hall(id);


--
-- Name: showtime showtime_movie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.showtime
    ADD CONSTRAINT showtime_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movie(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;


--
-- PostgreSQL database dump complete
--

