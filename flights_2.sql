--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.2

-- Started on 2024-04-15 17:53:35

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 218 (class 1259 OID 17495)
-- Name: flights_2; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.flights_2 (
    flight_id integer NOT NULL,
    airline character varying(255),
    flight_type character varying(770),
    from_dest character varying(255),
    to_dest character varying(255),
    arrival_time timestamp without time zone,
    flight_status character varying(50)
);


ALTER TABLE public.flights_2 OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 17494)
-- Name: flights_2_flight_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.flights_2_flight_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.flights_2_flight_id_seq OWNER TO postgres;

--
-- TOC entry 4790 (class 0 OID 0)
-- Dependencies: 217
-- Name: flights_2_flight_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.flights_2_flight_id_seq OWNED BY public.flights_2.flight_id;


--
-- TOC entry 4637 (class 2604 OID 17498)
-- Name: flights_2 flight_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.flights_2 ALTER COLUMN flight_id SET DEFAULT nextval('public.flights_2_flight_id_seq'::regclass);


--
-- TOC entry 4784 (class 0 OID 17495)
-- Dependencies: 218
-- Data for Name: flights_2; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.flights_2 (flight_id, airline, flight_type, from_dest, to_dest, arrival_time, flight_status) FROM stdin;
\.


--
-- TOC entry 4791 (class 0 OID 0)
-- Dependencies: 217
-- Name: flights_2_flight_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.flights_2_flight_id_seq', 1, false);


--
-- TOC entry 4639 (class 2606 OID 17502)
-- Name: flights_2 flights_2_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.flights_2
    ADD CONSTRAINT flights_2_pkey PRIMARY KEY (flight_id);


-- Completed on 2024-04-15 17:53:35

--
-- PostgreSQL database dump complete
--

