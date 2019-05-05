--
-- PostgreSQL database dump
--

-- Dumped from database version 10.5 (Ubuntu 10.5-1.pgdg18.04+1)
-- Dumped by pg_dump version 10.5 (Ubuntu 10.5-1.pgdg18.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: accounts_corruption; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.accounts_corruption (
    id integer NOT NULL,
    text text NOT NULL,
    author_profile_id integer,
    school_id integer
);


ALTER TABLE public.accounts_corruption OWNER TO admin;

--
-- Name: accounts_corruption_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.accounts_corruption_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_corruption_id_seq OWNER TO admin;

--
-- Name: accounts_corruption_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.accounts_corruption_id_seq OWNED BY public.accounts_corruption.id;


--
-- Name: accounts_crmcard; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.accounts_crmcard (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    phone character varying(250) NOT NULL,
    mail character varying(250) NOT NULL,
    comments character varying(250) NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    author_profile_id integer,
    column_id integer,
    school_id integer,
    saved boolean NOT NULL
);


ALTER TABLE public.accounts_crmcard OWNER TO admin;

--
-- Name: accounts_crmcard_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.accounts_crmcard_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_crmcard_id_seq OWNER TO admin;

--
-- Name: accounts_crmcard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.accounts_crmcard_id_seq OWNED BY public.accounts_crmcard.id;


--
-- Name: accounts_crmcolumn; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.accounts_crmcolumn (
    id integer NOT NULL,
    title character varying(250) NOT NULL,
    number_of_cards integer NOT NULL,
    school_id integer
);


ALTER TABLE public.accounts_crmcolumn OWNER TO admin;

--
-- Name: accounts_crmcolumn_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.accounts_crmcolumn_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_crmcolumn_id_seq OWNER TO admin;

--
-- Name: accounts_crmcolumn_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.accounts_crmcolumn_id_seq OWNED BY public.accounts_crmcolumn.id;


--
-- Name: accounts_jobcategory; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.accounts_jobcategory (
    id integer NOT NULL,
    title text,
    salary integer NOT NULL,
    profession_id integer NOT NULL
);


ALTER TABLE public.accounts_jobcategory OWNER TO admin;

--
-- Name: accounts_jobcategory_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.accounts_jobcategory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_jobcategory_id_seq OWNER TO admin;

--
-- Name: accounts_jobcategory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.accounts_jobcategory_id_seq OWNED BY public.accounts_jobcategory.id;


--
-- Name: accounts_misslesson; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.accounts_misslesson (
    id integer NOT NULL,
    text text,
    image character varying(100),
    height_field integer,
    width_field integer,
    dates date[] NOT NULL,
    profile_id integer
);


ALTER TABLE public.accounts_misslesson OWNER TO admin;

--
-- Name: accounts_misslesson_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.accounts_misslesson_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_misslesson_id_seq OWNER TO admin;

--
-- Name: accounts_misslesson_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.accounts_misslesson_id_seq OWNED BY public.accounts_misslesson.id;


--
-- Name: accounts_profession; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.accounts_profession (
    id integer NOT NULL,
    title text
);


ALTER TABLE public.accounts_profession OWNER TO admin;

--
-- Name: accounts_profession_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.accounts_profession_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_profession_id_seq OWNER TO admin;

--
-- Name: accounts_profession_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.accounts_profession_id_seq OWNED BY public.accounts_profession.id;


--
-- Name: accounts_profile; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.accounts_profile (
    id integer NOT NULL,
    coins integer NOT NULL,
    birthdate date,
    first_name text,
    phone text,
    image character varying(100),
    height_field integer,
    width_field integer,
    mail text NOT NULL,
    user_id integer NOT NULL,
    easy_skills integer[] NOT NULL,
    tag_ids integer[] NOT NULL,
    hard_skills integer[] NOT NULL,
    middle_skills integer[] NOT NULL,
    pro_skills integer[] NOT NULL,
    money integer NOT NULL,
    crm_age_id integer,
    crm_office_id integer,
    crm_subject_id integer,
    is_student boolean NOT NULL,
    hint integer NOT NULL
);


ALTER TABLE public.accounts_profile OWNER TO admin;

--
-- Name: accounts_profile_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.accounts_profile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_profile_id_seq OWNER TO admin;

--
-- Name: accounts_profile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.accounts_profile_id_seq OWNED BY public.accounts_profile.id;


--
-- Name: accounts_profile_job_categories; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.accounts_profile_job_categories (
    id integer NOT NULL,
    profile_id integer NOT NULL,
    jobcategory_id integer NOT NULL
);


ALTER TABLE public.accounts_profile_job_categories OWNER TO admin;

--
-- Name: accounts_profile_job_categories_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.accounts_profile_job_categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_profile_job_categories_id_seq OWNER TO admin;

--
-- Name: accounts_profile_job_categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.accounts_profile_job_categories_id_seq OWNED BY public.accounts_profile_job_categories.id;


--
-- Name: accounts_profile_profession; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.accounts_profile_profession (
    id integer NOT NULL,
    profile_id integer NOT NULL,
    profession_id integer NOT NULL
);


ALTER TABLE public.accounts_profile_profession OWNER TO admin;

--
-- Name: accounts_profile_profession_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.accounts_profile_profession_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_profile_profession_id_seq OWNER TO admin;

--
-- Name: accounts_profile_profession_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.accounts_profile_profession_id_seq OWNED BY public.accounts_profile_profession.id;


--
-- Name: accounts_profile_schools; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.accounts_profile_schools (
    id integer NOT NULL,
    profile_id integer NOT NULL,
    school_id integer NOT NULL
);


ALTER TABLE public.accounts_profile_schools OWNER TO admin;

--
-- Name: accounts_profile_schools_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.accounts_profile_schools_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_profile_schools_id_seq OWNER TO admin;

--
-- Name: accounts_profile_schools_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.accounts_profile_schools_id_seq OWNED BY public.accounts_profile_schools.id;


--
-- Name: accounts_zaiavka; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.accounts_zaiavka (
    id integer NOT NULL,
    first_name text NOT NULL,
    phone text,
    "timestamp" timestamp with time zone NOT NULL,
    mail text NOT NULL,
    school_id integer NOT NULL
);


ALTER TABLE public.accounts_zaiavka OWNER TO admin;

--
-- Name: accounts_zaiavka_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.accounts_zaiavka_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_zaiavka_id_seq OWNER TO admin;

--
-- Name: accounts_zaiavka_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.accounts_zaiavka_id_seq OWNED BY public.accounts_zaiavka.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO admin;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO admin;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO admin;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO admin;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO admin;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO admin;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO admin;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO admin;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO admin;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO admin;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO admin;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO admin;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO admin;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO admin;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO admin;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO admin;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO admin;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO admin;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO admin;

--
-- Name: docs_board; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.docs_board (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.docs_board OWNER TO admin;

--
-- Name: docs_board_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.docs_board_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.docs_board_id_seq OWNER TO admin;

--
-- Name: docs_board_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.docs_board_id_seq OWNED BY public.docs_board.id;


--
-- Name: docs_card; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.docs_card (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    slug character varying(50) NOT NULL,
    description text,
    column_id integer NOT NULL
);


ALTER TABLE public.docs_card OWNER TO admin;

--
-- Name: docs_card_doc_list; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.docs_card_doc_list (
    id integer NOT NULL,
    card_id integer NOT NULL,
    document_id integer NOT NULL
);


ALTER TABLE public.docs_card_doc_list OWNER TO admin;

--
-- Name: docs_card_doc_list_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.docs_card_doc_list_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.docs_card_doc_list_id_seq OWNER TO admin;

--
-- Name: docs_card_doc_list_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.docs_card_doc_list_id_seq OWNED BY public.docs_card_doc_list.id;


--
-- Name: docs_card_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.docs_card_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.docs_card_id_seq OWNER TO admin;

--
-- Name: docs_card_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.docs_card_id_seq OWNED BY public.docs_card.id;


--
-- Name: docs_card_metka_list; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.docs_card_metka_list (
    id integer NOT NULL,
    card_id integer NOT NULL,
    metka_id integer NOT NULL
);


ALTER TABLE public.docs_card_metka_list OWNER TO admin;

--
-- Name: docs_card_metka_list_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.docs_card_metka_list_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.docs_card_metka_list_id_seq OWNER TO admin;

--
-- Name: docs_card_metka_list_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.docs_card_metka_list_id_seq OWNED BY public.docs_card_metka_list.id;


--
-- Name: docs_card_user_list; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.docs_card_user_list (
    id integer NOT NULL,
    card_id integer NOT NULL,
    profile_id integer NOT NULL
);


ALTER TABLE public.docs_card_user_list OWNER TO admin;

--
-- Name: docs_card_user_list_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.docs_card_user_list_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.docs_card_user_list_id_seq OWNER TO admin;

--
-- Name: docs_card_user_list_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.docs_card_user_list_id_seq OWNED BY public.docs_card_user_list.id;


--
-- Name: docs_column; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.docs_column (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    board_id integer NOT NULL
);


ALTER TABLE public.docs_column OWNER TO admin;

--
-- Name: docs_column_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.docs_column_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.docs_column_id_seq OWNER TO admin;

--
-- Name: docs_column_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.docs_column_id_seq OWNED BY public.docs_column.id;


--
-- Name: docs_comment; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.docs_comment (
    id integer NOT NULL,
    content text NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    image character varying(100),
    height_field integer,
    width_field integer,
    author_profile_id integer NOT NULL,
    card_id integer NOT NULL
);


ALTER TABLE public.docs_comment OWNER TO admin;

--
-- Name: docs_comment_ffile; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.docs_comment_ffile (
    id integer NOT NULL,
    comment_id integer NOT NULL,
    document_id integer NOT NULL
);


ALTER TABLE public.docs_comment_ffile OWNER TO admin;

--
-- Name: docs_comment_ffile_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.docs_comment_ffile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.docs_comment_ffile_id_seq OWNER TO admin;

--
-- Name: docs_comment_ffile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.docs_comment_ffile_id_seq OWNED BY public.docs_comment_ffile.id;


--
-- Name: docs_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.docs_comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.docs_comment_id_seq OWNER TO admin;

--
-- Name: docs_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.docs_comment_id_seq OWNED BY public.docs_comment.id;


--
-- Name: docs_document; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.docs_document (
    id integer NOT NULL,
    file character varying(100)
);


ALTER TABLE public.docs_document OWNER TO admin;

--
-- Name: docs_document_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.docs_document_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.docs_document_id_seq OWNER TO admin;

--
-- Name: docs_document_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.docs_document_id_seq OWNED BY public.docs_document.id;


--
-- Name: docs_metka; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.docs_metka (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.docs_metka OWNER TO admin;

--
-- Name: docs_metka_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.docs_metka_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.docs_metka_id_seq OWNER TO admin;

--
-- Name: docs_metka_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.docs_metka_id_seq OWNED BY public.docs_metka.id;


--
-- Name: documents_documentcache; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.documents_documentcache (
    id integer NOT NULL,
    object_type text NOT NULL,
    object_id integer,
    action text NOT NULL,
    previous_parent integer,
    "timestamp" timestamp with time zone NOT NULL,
    "full" boolean NOT NULL,
    author_profile_id integer
);


ALTER TABLE public.documents_documentcache OWNER TO admin;

--
-- Name: documents_documentcache_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.documents_documentcache_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.documents_documentcache_id_seq OWNER TO admin;

--
-- Name: documents_documentcache_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.documents_documentcache_id_seq OWNED BY public.documents_documentcache.id;


--
-- Name: documents_documentfolder; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.documents_documentfolder (
    id integer NOT NULL,
    title text NOT NULL,
    author_profile_id integer,
    parent_id integer,
    school_id integer NOT NULL
);


ALTER TABLE public.documents_documentfolder OWNER TO admin;

--
-- Name: documents_documentfolder_children; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.documents_documentfolder_children (
    id integer NOT NULL,
    from_documentfolder_id integer NOT NULL,
    to_documentfolder_id integer NOT NULL
);


ALTER TABLE public.documents_documentfolder_children OWNER TO admin;

--
-- Name: documents_documentfolder_children_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.documents_documentfolder_children_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.documents_documentfolder_children_id_seq OWNER TO admin;

--
-- Name: documents_documentfolder_children_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.documents_documentfolder_children_id_seq OWNED BY public.documents_documentfolder_children.id;


--
-- Name: documents_documentfolder_files; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.documents_documentfolder_files (
    id integer NOT NULL,
    documentfolder_id integer NOT NULL,
    document_id integer NOT NULL
);


ALTER TABLE public.documents_documentfolder_files OWNER TO admin;

--
-- Name: documents_documentfolder_files_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.documents_documentfolder_files_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.documents_documentfolder_files_id_seq OWNER TO admin;

--
-- Name: documents_documentfolder_files_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.documents_documentfolder_files_id_seq OWNED BY public.documents_documentfolder_files.id;


--
-- Name: documents_documentfolder_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.documents_documentfolder_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.documents_documentfolder_id_seq OWNER TO admin;

--
-- Name: documents_documentfolder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.documents_documentfolder_id_seq OWNED BY public.documents_documentfolder.id;


--
-- Name: library_cache; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.library_cache (
    id integer NOT NULL,
    object_type text NOT NULL,
    object_id integer,
    action text NOT NULL,
    previous_parent integer,
    "timestamp" timestamp with time zone NOT NULL,
    "full" boolean NOT NULL,
    author_profile_id integer
);


ALTER TABLE public.library_cache OWNER TO admin;

--
-- Name: library_cache_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.library_cache_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.library_cache_id_seq OWNER TO admin;

--
-- Name: library_cache_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.library_cache_id_seq OWNED BY public.library_cache.id;


--
-- Name: library_folder; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.library_folder (
    id integer NOT NULL,
    title text NOT NULL,
    author_profile_id integer,
    parent_id integer,
    school_id integer NOT NULL
);


ALTER TABLE public.library_folder OWNER TO admin;

--
-- Name: library_folder_children; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.library_folder_children (
    id integer NOT NULL,
    from_folder_id integer NOT NULL,
    to_folder_id integer NOT NULL
);


ALTER TABLE public.library_folder_children OWNER TO admin;

--
-- Name: library_folder_children_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.library_folder_children_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.library_folder_children_id_seq OWNER TO admin;

--
-- Name: library_folder_children_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.library_folder_children_id_seq OWNED BY public.library_folder_children.id;


--
-- Name: library_folder_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.library_folder_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.library_folder_id_seq OWNER TO admin;

--
-- Name: library_folder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.library_folder_id_seq OWNED BY public.library_folder.id;


--
-- Name: library_folder_lesson_list; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.library_folder_lesson_list (
    id integer NOT NULL,
    folder_id integer NOT NULL,
    lesson_id integer NOT NULL
);


ALTER TABLE public.library_folder_lesson_list OWNER TO admin;

--
-- Name: library_folder_lesson_list_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.library_folder_lesson_list_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.library_folder_lesson_list_id_seq OWNER TO admin;

--
-- Name: library_folder_lesson_list_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.library_folder_lesson_list_id_seq OWNED BY public.library_folder_lesson_list.id;


--
-- Name: news_post; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.news_post (
    id integer NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    content text NOT NULL,
    image character varying(100),
    height_field integer,
    width_field integer,
    author_profile_id integer NOT NULL,
    school_id integer NOT NULL
);


ALTER TABLE public.news_post OWNER TO admin;

--
-- Name: news_post_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.news_post_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.news_post_id_seq OWNER TO admin;

--
-- Name: news_post_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.news_post_id_seq OWNED BY public.news_post.id;


--
-- Name: papers_comment; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.papers_comment (
    id integer NOT NULL,
    level integer NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    content text NOT NULL,
    author_profile_id integer,
    lesson_id integer,
    parent_id integer
);


ALTER TABLE public.papers_comment OWNER TO admin;

--
-- Name: papers_comment_dislikes; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.papers_comment_dislikes (
    id integer NOT NULL,
    comment_id integer NOT NULL,
    profile_id integer NOT NULL
);


ALTER TABLE public.papers_comment_dislikes OWNER TO admin;

--
-- Name: papers_comment_dislikes_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.papers_comment_dislikes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.papers_comment_dislikes_id_seq OWNER TO admin;

--
-- Name: papers_comment_dislikes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.papers_comment_dislikes_id_seq OWNED BY public.papers_comment_dislikes.id;


--
-- Name: papers_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.papers_comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.papers_comment_id_seq OWNER TO admin;

--
-- Name: papers_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.papers_comment_id_seq OWNED BY public.papers_comment.id;


--
-- Name: papers_comment_likes; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.papers_comment_likes (
    id integer NOT NULL,
    comment_id integer NOT NULL,
    profile_id integer NOT NULL
);


ALTER TABLE public.papers_comment_likes OWNER TO admin;

--
-- Name: papers_comment_likes_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.papers_comment_likes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.papers_comment_likes_id_seq OWNER TO admin;

--
-- Name: papers_comment_likes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.papers_comment_likes_id_seq OWNED BY public.papers_comment_likes.id;


--
-- Name: papers_course; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.papers_course (
    id integer NOT NULL,
    title character varying(250) NOT NULL,
    image character varying(100),
    height_field integer,
    width_field integer,
    content text NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    author_profile_id integer,
    cost integer NOT NULL,
    stars integer[] NOT NULL,
    rating double precision NOT NULL,
    school_id integer NOT NULL
);


ALTER TABLE public.papers_course OWNER TO admin;

--
-- Name: papers_course_done_by; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.papers_course_done_by (
    id integer NOT NULL,
    course_id integer NOT NULL,
    profile_id integer NOT NULL
);


ALTER TABLE public.papers_course_done_by OWNER TO admin;

--
-- Name: papers_course_done_by_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.papers_course_done_by_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.papers_course_done_by_id_seq OWNER TO admin;

--
-- Name: papers_course_done_by_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.papers_course_done_by_id_seq OWNED BY public.papers_course_done_by.id;


--
-- Name: papers_course_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.papers_course_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.papers_course_id_seq OWNER TO admin;

--
-- Name: papers_course_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.papers_course_id_seq OWNED BY public.papers_course.id;


--
-- Name: papers_course_lessons; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.papers_course_lessons (
    id integer NOT NULL,
    course_id integer NOT NULL,
    lesson_id integer NOT NULL
);


ALTER TABLE public.papers_course_lessons OWNER TO admin;

--
-- Name: papers_course_lesson_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.papers_course_lesson_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.papers_course_lesson_id_seq OWNER TO admin;

--
-- Name: papers_course_lesson_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.papers_course_lesson_id_seq OWNED BY public.papers_course_lessons.id;


--
-- Name: papers_course_students; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.papers_course_students (
    id integer NOT NULL,
    course_id integer NOT NULL,
    profile_id integer NOT NULL
);


ALTER TABLE public.papers_course_students OWNER TO admin;

--
-- Name: papers_course_students_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.papers_course_students_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.papers_course_students_id_seq OWNER TO admin;

--
-- Name: papers_course_students_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.papers_course_students_id_seq OWNED BY public.papers_course_students.id;


--
-- Name: papers_lesson; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.papers_lesson (
    id integer NOT NULL,
    title character varying(250) NOT NULL,
    is_homework boolean NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    author_profile_id integer,
    rating integer NOT NULL,
    estimater_ids integer[] NOT NULL,
    grades integer[] NOT NULL,
    school_id integer NOT NULL,
    access_to_everyone boolean NOT NULL
);


ALTER TABLE public.papers_lesson OWNER TO admin;

--
-- Name: papers_lesson_done_by; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.papers_lesson_done_by (
    id integer NOT NULL,
    lesson_id integer NOT NULL,
    profile_id integer NOT NULL
);


ALTER TABLE public.papers_lesson_done_by OWNER TO admin;

--
-- Name: papers_lesson_done_by_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.papers_lesson_done_by_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.papers_lesson_done_by_id_seq OWNER TO admin;

--
-- Name: papers_lesson_done_by_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.papers_lesson_done_by_id_seq OWNED BY public.papers_lesson_done_by.id;


--
-- Name: papers_lesson_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.papers_lesson_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.papers_lesson_id_seq OWNER TO admin;

--
-- Name: papers_lesson_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.papers_lesson_id_seq OWNED BY public.papers_lesson.id;


--
-- Name: papers_lesson_papers; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.papers_lesson_papers (
    id integer NOT NULL,
    lesson_id integer NOT NULL,
    paper_id integer NOT NULL
);


ALTER TABLE public.papers_lesson_papers OWNER TO admin;

--
-- Name: papers_lesson_papers_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.papers_lesson_papers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.papers_lesson_papers_id_seq OWNER TO admin;

--
-- Name: papers_lesson_papers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.papers_lesson_papers_id_seq OWNED BY public.papers_lesson_papers.id;


--
-- Name: papers_paper; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.papers_paper (
    id integer NOT NULL,
    title character varying(250) NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    author_profile_id integer,
    typee character varying(250) NOT NULL,
    school_id integer NOT NULL
);


ALTER TABLE public.papers_paper OWNER TO admin;

--
-- Name: papers_paper_done_by; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.papers_paper_done_by (
    id integer NOT NULL,
    paper_id integer NOT NULL,
    profile_id integer NOT NULL
);


ALTER TABLE public.papers_paper_done_by OWNER TO admin;

--
-- Name: papers_paper_done_by_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.papers_paper_done_by_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.papers_paper_done_by_id_seq OWNER TO admin;

--
-- Name: papers_paper_done_by_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.papers_paper_done_by_id_seq OWNED BY public.papers_paper_done_by.id;


--
-- Name: papers_paper_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.papers_paper_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.papers_paper_id_seq OWNER TO admin;

--
-- Name: papers_paper_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.papers_paper_id_seq OWNED BY public.papers_paper.id;


--
-- Name: papers_paper_subthemes; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.papers_paper_subthemes (
    id integer NOT NULL,
    paper_id integer NOT NULL,
    subtheme_id integer NOT NULL
);


ALTER TABLE public.papers_paper_subthemes OWNER TO admin;

--
-- Name: papers_paper_subthemes_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.papers_paper_subthemes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.papers_paper_subthemes_id_seq OWNER TO admin;

--
-- Name: papers_paper_subthemes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.papers_paper_subthemes_id_seq OWNED BY public.papers_paper_subthemes.id;


--
-- Name: papers_subtheme; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.papers_subtheme (
    id integer NOT NULL,
    content text NOT NULL,
    video character varying(100) NOT NULL,
    file character varying(100) NOT NULL,
    youtube_video_link text NOT NULL
);


ALTER TABLE public.papers_subtheme OWNER TO admin;

--
-- Name: papers_subtheme_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.papers_subtheme_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.papers_subtheme_id_seq OWNER TO admin;

--
-- Name: papers_subtheme_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.papers_subtheme_id_seq OWNED BY public.papers_subtheme.id;


--
-- Name: papers_subtheme_task_list; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.papers_subtheme_task_list (
    id integer NOT NULL,
    subtheme_id integer NOT NULL,
    task_id integer NOT NULL
);


ALTER TABLE public.papers_subtheme_task_list OWNER TO admin;

--
-- Name: papers_subtheme_task_list_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.papers_subtheme_task_list_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.papers_subtheme_task_list_id_seq OWNER TO admin;

--
-- Name: papers_subtheme_task_list_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.papers_subtheme_task_list_id_seq OWNED BY public.papers_subtheme_task_list.id;


--
-- Name: schools_cabinet; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.schools_cabinet (
    id integer NOT NULL,
    title character varying(250) NOT NULL,
    capacity integer NOT NULL,
    school_id integer
);


ALTER TABLE public.schools_cabinet OWNER TO admin;

--
-- Name: schools_cabinett_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.schools_cabinett_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.schools_cabinett_id_seq OWNER TO admin;

--
-- Name: schools_cabinett_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.schools_cabinett_id_seq OWNED BY public.schools_cabinet.id;


--
-- Name: schools_office; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.schools_office (
    id integer NOT NULL,
    title character varying(250) NOT NULL,
    address text NOT NULL,
    capacity integer NOT NULL,
    school_id integer
);


ALTER TABLE public.schools_office OWNER TO admin;

--
-- Name: schools_office_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.schools_office_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.schools_office_id_seq OWNER TO admin;

--
-- Name: schools_office_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.schools_office_id_seq OWNED BY public.schools_office.id;


--
-- Name: schools_school; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.schools_school (
    id integer NOT NULL,
    title character varying(250) NOT NULL,
    image_icon character varying(100),
    height_field integer,
    width_field integer,
    image_banner character varying(100),
    height_field2 integer,
    width_field2 integer,
    content text NOT NULL,
    slogan character varying(250) NOT NULL,
    new_schedule boolean NOT NULL,
    official_school boolean NOT NULL
);


ALTER TABLE public.schools_school OWNER TO admin;

--
-- Name: schools_school_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.schools_school_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.schools_school_id_seq OWNER TO admin;

--
-- Name: schools_school_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.schools_school_id_seq OWNED BY public.schools_school.id;


--
-- Name: schools_subjectage; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.schools_subjectage (
    id integer NOT NULL,
    title character varying(250) NOT NULL,
    school_id integer
);


ALTER TABLE public.schools_subjectage OWNER TO admin;

--
-- Name: schools_subjectage_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.schools_subjectage_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.schools_subjectage_id_seq OWNER TO admin;

--
-- Name: schools_subjectage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.schools_subjectage_id_seq OWNED BY public.schools_subjectage.id;


--
-- Name: schools_subjectcategory; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.schools_subjectcategory (
    id integer NOT NULL,
    title character varying(250) NOT NULL,
    school_id integer
);


ALTER TABLE public.schools_subjectcategory OWNER TO admin;

--
-- Name: schools_subjectcategory_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.schools_subjectcategory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.schools_subjectcategory_id_seq OWNER TO admin;

--
-- Name: schools_subjectcategory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.schools_subjectcategory_id_seq OWNED BY public.schools_subjectcategory.id;


--
-- Name: squads_squad; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.squads_squad (
    id integer NOT NULL,
    title character varying(250) NOT NULL,
    slug character varying(50) NOT NULL,
    image_banner character varying(100),
    height_field integer,
    width_field integer,
    content text NOT NULL,
    slogan character varying(250) NOT NULL,
    end_date date NOT NULL,
    start_date date NOT NULL,
    image_icon character varying(100),
    school_id integer NOT NULL,
    color_back text NOT NULL
);


ALTER TABLE public.squads_squad OWNER TO admin;

--
-- Name: squads_squad_curator; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.squads_squad_curator (
    id integer NOT NULL,
    squad_id integer NOT NULL,
    profile_id integer NOT NULL
);


ALTER TABLE public.squads_squad_curator OWNER TO admin;

--
-- Name: squads_squad_curator_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.squads_squad_curator_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.squads_squad_curator_id_seq OWNER TO admin;

--
-- Name: squads_squad_curator_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.squads_squad_curator_id_seq OWNED BY public.squads_squad_curator.id;


--
-- Name: squads_squad_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.squads_squad_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.squads_squad_id_seq OWNER TO admin;

--
-- Name: squads_squad_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.squads_squad_id_seq OWNED BY public.squads_squad.id;


--
-- Name: squads_squad_students; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.squads_squad_students (
    id integer NOT NULL,
    squad_id integer NOT NULL,
    profile_id integer NOT NULL
);


ALTER TABLE public.squads_squad_students OWNER TO admin;

--
-- Name: squads_squad_students_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.squads_squad_students_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.squads_squad_students_id_seq OWNER TO admin;

--
-- Name: squads_squad_students_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.squads_squad_students_id_seq OWNED BY public.squads_squad_students.id;


--
-- Name: subjects_attendance; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.subjects_attendance (
    id integer NOT NULL,
    present text NOT NULL,
    grade integer NOT NULL,
    student_id integer NOT NULL,
    subject_id integer,
    squad_id integer,
    subject_materials_id integer,
    teacher_id integer NOT NULL,
    school_id integer NOT NULL
);


ALTER TABLE public.subjects_attendance OWNER TO admin;

--
-- Name: subjects_attendance_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.subjects_attendance_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subjects_attendance_id_seq OWNER TO admin;

--
-- Name: subjects_attendance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.subjects_attendance_id_seq OWNED BY public.subjects_attendance.id;


--
-- Name: subjects_cacheattendance; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.subjects_cacheattendance (
    id integer NOT NULL,
    profile_id integer,
    squad_id integer,
    subject_id integer
);


ALTER TABLE public.subjects_cacheattendance OWNER TO admin;

--
-- Name: subjects_cacheattendance_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.subjects_cacheattendance_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subjects_cacheattendance_id_seq OWNER TO admin;

--
-- Name: subjects_cacheattendance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.subjects_cacheattendance_id_seq OWNED BY public.subjects_cacheattendance.id;


--
-- Name: subjects_cell; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.subjects_cell (
    id integer NOT NULL,
    day_id integer,
    time_period_id integer,
    school_id integer NOT NULL
);


ALTER TABLE public.subjects_cell OWNER TO admin;

--
-- Name: subjects_cell_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.subjects_cell_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subjects_cell_id_seq OWNER TO admin;

--
-- Name: subjects_cell_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.subjects_cell_id_seq OWNED BY public.subjects_cell.id;


--
-- Name: subjects_day; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.subjects_day (
    id integer NOT NULL,
    title text NOT NULL,
    number integer NOT NULL
);


ALTER TABLE public.subjects_day OWNER TO admin;

--
-- Name: subjects_day_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.subjects_day_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subjects_day_id_seq OWNER TO admin;

--
-- Name: subjects_day_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.subjects_day_id_seq OWNED BY public.subjects_day.id;


--
-- Name: subjects_lecture; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.subjects_lecture (
    id integer NOT NULL,
    cell_id integer,
    squad_id integer,
    subject_id integer,
    school_id integer NOT NULL,
    cabinet_id integer,
    day_id integer,
    age_id integer,
    category_id integer,
    office_id integer
);


ALTER TABLE public.subjects_lecture OWNER TO admin;

--
-- Name: subjects_lecture_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.subjects_lecture_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subjects_lecture_id_seq OWNER TO admin;

--
-- Name: subjects_lecture_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.subjects_lecture_id_seq OWNED BY public.subjects_lecture.id;


--
-- Name: subjects_lecture_people; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.subjects_lecture_people (
    id integer NOT NULL,
    lecture_id integer NOT NULL,
    profile_id integer NOT NULL
);


ALTER TABLE public.subjects_lecture_people OWNER TO admin;

--
-- Name: subjects_lecture_people_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.subjects_lecture_people_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subjects_lecture_people_id_seq OWNER TO admin;

--
-- Name: subjects_lecture_people_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.subjects_lecture_people_id_seq OWNED BY public.subjects_lecture_people.id;


--
-- Name: subjects_subject; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.subjects_subject (
    id integer NOT NULL,
    title character varying(250) NOT NULL,
    slug character varying(50) NOT NULL,
    image_banner character varying(100),
    height_field integer,
    width_field integer,
    content text NOT NULL,
    slogan character varying(250) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    number_of_lectures integer NOT NULL,
    image_icon character varying(100),
    height_field2 integer,
    height_field3 integer,
    image_back character varying(100),
    width_field2 integer,
    width_field3 integer,
    color_back text NOT NULL,
    school_id integer NOT NULL,
    age_id integer,
    category_id integer,
    office_id integer,
    cost integer,
    squad_ids integer[] NOT NULL,
    start_dates date[] NOT NULL
);


ALTER TABLE public.subjects_subject OWNER TO admin;

--
-- Name: subjects_subject_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.subjects_subject_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subjects_subject_id_seq OWNER TO admin;

--
-- Name: subjects_subject_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.subjects_subject_id_seq OWNED BY public.subjects_subject.id;


--
-- Name: subjects_subject_squads; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.subjects_subject_squads (
    id integer NOT NULL,
    subject_id integer NOT NULL,
    squad_id integer NOT NULL
);


ALTER TABLE public.subjects_subject_squads OWNER TO admin;

--
-- Name: subjects_subject_squads_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.subjects_subject_squads_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subjects_subject_squads_id_seq OWNER TO admin;

--
-- Name: subjects_subject_squads_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.subjects_subject_squads_id_seq OWNED BY public.subjects_subject_squads.id;


--
-- Name: subjects_subject_students; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.subjects_subject_students (
    id integer NOT NULL,
    subject_id integer NOT NULL,
    profile_id integer NOT NULL
);


ALTER TABLE public.subjects_subject_students OWNER TO admin;

--
-- Name: subjects_subject_students_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.subjects_subject_students_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subjects_subject_students_id_seq OWNER TO admin;

--
-- Name: subjects_subject_students_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.subjects_subject_students_id_seq OWNED BY public.subjects_subject_students.id;


--
-- Name: subjects_subject_teacher; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.subjects_subject_teacher (
    id integer NOT NULL,
    subject_id integer NOT NULL,
    profile_id integer NOT NULL
);


ALTER TABLE public.subjects_subject_teacher OWNER TO admin;

--
-- Name: subjects_subject_teacher_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.subjects_subject_teacher_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subjects_subject_teacher_id_seq OWNER TO admin;

--
-- Name: subjects_subject_teacher_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.subjects_subject_teacher_id_seq OWNED BY public.subjects_subject_teacher.id;


--
-- Name: subjects_subjectmaterials; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.subjects_subjectmaterials (
    id integer NOT NULL,
    number integer NOT NULL,
    subject_id integer,
    school_id integer NOT NULL
);


ALTER TABLE public.subjects_subjectmaterials OWNER TO admin;

--
-- Name: subjects_subjectmaterials_done_by; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.subjects_subjectmaterials_done_by (
    id integer NOT NULL,
    subjectmaterials_id integer NOT NULL,
    profile_id integer NOT NULL
);


ALTER TABLE public.subjects_subjectmaterials_done_by OWNER TO admin;

--
-- Name: subjects_subjectmaterials_done_by_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.subjects_subjectmaterials_done_by_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subjects_subjectmaterials_done_by_id_seq OWNER TO admin;

--
-- Name: subjects_subjectmaterials_done_by_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.subjects_subjectmaterials_done_by_id_seq OWNED BY public.subjects_subjectmaterials_done_by.id;


--
-- Name: subjects_subjectmaterials_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.subjects_subjectmaterials_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subjects_subjectmaterials_id_seq OWNER TO admin;

--
-- Name: subjects_subjectmaterials_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.subjects_subjectmaterials_id_seq OWNED BY public.subjects_subjectmaterials.id;


--
-- Name: subjects_subjectmaterials_lessons; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.subjects_subjectmaterials_lessons (
    id integer NOT NULL,
    subjectmaterials_id integer NOT NULL,
    lesson_id integer NOT NULL
);


ALTER TABLE public.subjects_subjectmaterials_lessons OWNER TO admin;

--
-- Name: subjects_subjectmaterials_lessons_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.subjects_subjectmaterials_lessons_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subjects_subjectmaterials_lessons_id_seq OWNER TO admin;

--
-- Name: subjects_subjectmaterials_lessons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.subjects_subjectmaterials_lessons_id_seq OWNED BY public.subjects_subjectmaterials_lessons.id;


--
-- Name: subjects_timeperiod; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.subjects_timeperiod (
    id integer NOT NULL,
    start text NOT NULL,
    "end" text NOT NULL,
    num integer NOT NULL,
    school_id integer NOT NULL
);


ALTER TABLE public.subjects_timeperiod OWNER TO admin;

--
-- Name: subjects_timeperiod_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.subjects_timeperiod_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subjects_timeperiod_id_seq OWNER TO admin;

--
-- Name: subjects_timeperiod_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.subjects_timeperiod_id_seq OWNED BY public.subjects_timeperiod.id;


--
-- Name: subjects_timeperiod_people; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.subjects_timeperiod_people (
    id integer NOT NULL,
    timeperiod_id integer NOT NULL,
    profile_id integer NOT NULL
);


ALTER TABLE public.subjects_timeperiod_people OWNER TO admin;

--
-- Name: subjects_timeperiod_students_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.subjects_timeperiod_students_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subjects_timeperiod_students_id_seq OWNER TO admin;

--
-- Name: subjects_timeperiod_students_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.subjects_timeperiod_students_id_seq OWNED BY public.subjects_timeperiod_people.id;


--
-- Name: tasks_problemtag; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.tasks_problemtag (
    id integer NOT NULL,
    title text NOT NULL
);


ALTER TABLE public.tasks_problemtag OWNER TO admin;

--
-- Name: tasks_problemtag_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.tasks_problemtag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tasks_problemtag_id_seq OWNER TO admin;

--
-- Name: tasks_problemtag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.tasks_problemtag_id_seq OWNED BY public.tasks_problemtag.id;


--
-- Name: tasks_solver; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.tasks_solver (
    id integer NOT NULL,
    solver_ans text[] NOT NULL,
    solver_correctness boolean NOT NULL,
    solver_try_number integer NOT NULL,
    author_profile_id integer NOT NULL,
    task_id integer NOT NULL
);


ALTER TABLE public.tasks_solver OWNER TO admin;

--
-- Name: tasks_solver_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.tasks_solver_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tasks_solver_id_seq OWNER TO admin;

--
-- Name: tasks_solver_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.tasks_solver_id_seq OWNED BY public.tasks_solver.id;


--
-- Name: tasks_task; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.tasks_task (
    id integer NOT NULL,
    slug character varying(50) NOT NULL,
    text text NOT NULL,
    image character varying(100),
    height_field integer,
    width_field integer,
    answer text[] NOT NULL,
    cost integer NOT NULL,
    is_test boolean NOT NULL,
    is_mult_ans boolean NOT NULL,
    variants text[] NOT NULL,
    author_profile_id integer NOT NULL,
    parent_id integer
);


ALTER TABLE public.tasks_task OWNER TO admin;

--
-- Name: tasks_task_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.tasks_task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tasks_task_id_seq OWNER TO admin;

--
-- Name: tasks_task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.tasks_task_id_seq OWNED BY public.tasks_task.id;


--
-- Name: tasks_task_tags; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.tasks_task_tags (
    id integer NOT NULL,
    task_id integer NOT NULL,
    problemtag_id integer NOT NULL
);


ALTER TABLE public.tasks_task_tags OWNER TO admin;

--
-- Name: tasks_task_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.tasks_task_tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tasks_task_tags_id_seq OWNER TO admin;

--
-- Name: tasks_task_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.tasks_task_tags_id_seq OWNED BY public.tasks_task_tags.id;


--
-- Name: todolist_board; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.todolist_board (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    school_id integer NOT NULL
);


ALTER TABLE public.todolist_board OWNER TO admin;

--
-- Name: todolist_board_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.todolist_board_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.todolist_board_id_seq OWNER TO admin;

--
-- Name: todolist_board_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.todolist_board_id_seq OWNED BY public.todolist_board.id;


--
-- Name: todolist_card; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.todolist_card (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    slug character varying(50) NOT NULL,
    description text,
    column_id integer NOT NULL
);


ALTER TABLE public.todolist_card OWNER TO admin;

--
-- Name: todolist_card_doc_list; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.todolist_card_doc_list (
    id integer NOT NULL,
    card_id integer NOT NULL,
    document_id integer NOT NULL
);


ALTER TABLE public.todolist_card_doc_list OWNER TO admin;

--
-- Name: todolist_card_doc_list_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.todolist_card_doc_list_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.todolist_card_doc_list_id_seq OWNER TO admin;

--
-- Name: todolist_card_doc_list_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.todolist_card_doc_list_id_seq OWNED BY public.todolist_card_doc_list.id;


--
-- Name: todolist_card_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.todolist_card_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.todolist_card_id_seq OWNER TO admin;

--
-- Name: todolist_card_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.todolist_card_id_seq OWNED BY public.todolist_card.id;


--
-- Name: todolist_card_metka_list; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.todolist_card_metka_list (
    id integer NOT NULL,
    card_id integer NOT NULL,
    metka_id integer NOT NULL
);


ALTER TABLE public.todolist_card_metka_list OWNER TO admin;

--
-- Name: todolist_card_metka_list_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.todolist_card_metka_list_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.todolist_card_metka_list_id_seq OWNER TO admin;

--
-- Name: todolist_card_metka_list_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.todolist_card_metka_list_id_seq OWNED BY public.todolist_card_metka_list.id;


--
-- Name: todolist_card_user_list; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.todolist_card_user_list (
    id integer NOT NULL,
    card_id integer NOT NULL,
    profile_id integer NOT NULL
);


ALTER TABLE public.todolist_card_user_list OWNER TO admin;

--
-- Name: todolist_card_user_list_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.todolist_card_user_list_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.todolist_card_user_list_id_seq OWNER TO admin;

--
-- Name: todolist_card_user_list_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.todolist_card_user_list_id_seq OWNED BY public.todolist_card_user_list.id;


--
-- Name: todolist_column; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.todolist_column (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    board_id integer NOT NULL
);


ALTER TABLE public.todolist_column OWNER TO admin;

--
-- Name: todolist_column_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.todolist_column_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.todolist_column_id_seq OWNER TO admin;

--
-- Name: todolist_column_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.todolist_column_id_seq OWNED BY public.todolist_column.id;


--
-- Name: todolist_comment; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.todolist_comment (
    id integer NOT NULL,
    content text NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    image character varying(100),
    height_field integer,
    width_field integer,
    author_profile_id integer NOT NULL,
    card_id integer NOT NULL
);


ALTER TABLE public.todolist_comment OWNER TO admin;

--
-- Name: todolist_comment_ffile; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.todolist_comment_ffile (
    id integer NOT NULL,
    comment_id integer NOT NULL,
    document_id integer NOT NULL
);


ALTER TABLE public.todolist_comment_ffile OWNER TO admin;

--
-- Name: todolist_comment_ffile_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.todolist_comment_ffile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.todolist_comment_ffile_id_seq OWNER TO admin;

--
-- Name: todolist_comment_ffile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.todolist_comment_ffile_id_seq OWNED BY public.todolist_comment_ffile.id;


--
-- Name: todolist_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.todolist_comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.todolist_comment_id_seq OWNER TO admin;

--
-- Name: todolist_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.todolist_comment_id_seq OWNED BY public.todolist_comment.id;


--
-- Name: todolist_document; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.todolist_document (
    id integer NOT NULL,
    file character varying(100),
    object_type character varying(255) NOT NULL,
    school_id integer NOT NULL
);


ALTER TABLE public.todolist_document OWNER TO admin;

--
-- Name: todolist_document_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.todolist_document_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.todolist_document_id_seq OWNER TO admin;

--
-- Name: todolist_document_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.todolist_document_id_seq OWNED BY public.todolist_document.id;


--
-- Name: todolist_metka; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.todolist_metka (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.todolist_metka OWNER TO admin;

--
-- Name: todolist_metka_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.todolist_metka_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.todolist_metka_id_seq OWNER TO admin;

--
-- Name: todolist_metka_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.todolist_metka_id_seq OWNED BY public.todolist_metka.id;


--
-- Name: accounts_corruption id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_corruption ALTER COLUMN id SET DEFAULT nextval('public.accounts_corruption_id_seq'::regclass);


--
-- Name: accounts_crmcard id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_crmcard ALTER COLUMN id SET DEFAULT nextval('public.accounts_crmcard_id_seq'::regclass);


--
-- Name: accounts_crmcolumn id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_crmcolumn ALTER COLUMN id SET DEFAULT nextval('public.accounts_crmcolumn_id_seq'::regclass);


--
-- Name: accounts_jobcategory id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_jobcategory ALTER COLUMN id SET DEFAULT nextval('public.accounts_jobcategory_id_seq'::regclass);


--
-- Name: accounts_misslesson id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_misslesson ALTER COLUMN id SET DEFAULT nextval('public.accounts_misslesson_id_seq'::regclass);


--
-- Name: accounts_profession id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profession ALTER COLUMN id SET DEFAULT nextval('public.accounts_profession_id_seq'::regclass);


--
-- Name: accounts_profile id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profile ALTER COLUMN id SET DEFAULT nextval('public.accounts_profile_id_seq'::regclass);


--
-- Name: accounts_profile_job_categories id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profile_job_categories ALTER COLUMN id SET DEFAULT nextval('public.accounts_profile_job_categories_id_seq'::regclass);


--
-- Name: accounts_profile_profession id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profile_profession ALTER COLUMN id SET DEFAULT nextval('public.accounts_profile_profession_id_seq'::regclass);


--
-- Name: accounts_profile_schools id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profile_schools ALTER COLUMN id SET DEFAULT nextval('public.accounts_profile_schools_id_seq'::regclass);


--
-- Name: accounts_zaiavka id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_zaiavka ALTER COLUMN id SET DEFAULT nextval('public.accounts_zaiavka_id_seq'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: docs_board id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_board ALTER COLUMN id SET DEFAULT nextval('public.docs_board_id_seq'::regclass);


--
-- Name: docs_card id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_card ALTER COLUMN id SET DEFAULT nextval('public.docs_card_id_seq'::regclass);


--
-- Name: docs_card_doc_list id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_card_doc_list ALTER COLUMN id SET DEFAULT nextval('public.docs_card_doc_list_id_seq'::regclass);


--
-- Name: docs_card_metka_list id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_card_metka_list ALTER COLUMN id SET DEFAULT nextval('public.docs_card_metka_list_id_seq'::regclass);


--
-- Name: docs_card_user_list id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_card_user_list ALTER COLUMN id SET DEFAULT nextval('public.docs_card_user_list_id_seq'::regclass);


--
-- Name: docs_column id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_column ALTER COLUMN id SET DEFAULT nextval('public.docs_column_id_seq'::regclass);


--
-- Name: docs_comment id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_comment ALTER COLUMN id SET DEFAULT nextval('public.docs_comment_id_seq'::regclass);


--
-- Name: docs_comment_ffile id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_comment_ffile ALTER COLUMN id SET DEFAULT nextval('public.docs_comment_ffile_id_seq'::regclass);


--
-- Name: docs_document id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_document ALTER COLUMN id SET DEFAULT nextval('public.docs_document_id_seq'::regclass);


--
-- Name: docs_metka id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_metka ALTER COLUMN id SET DEFAULT nextval('public.docs_metka_id_seq'::regclass);


--
-- Name: documents_documentcache id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.documents_documentcache ALTER COLUMN id SET DEFAULT nextval('public.documents_documentcache_id_seq'::regclass);


--
-- Name: documents_documentfolder id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.documents_documentfolder ALTER COLUMN id SET DEFAULT nextval('public.documents_documentfolder_id_seq'::regclass);


--
-- Name: documents_documentfolder_children id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.documents_documentfolder_children ALTER COLUMN id SET DEFAULT nextval('public.documents_documentfolder_children_id_seq'::regclass);


--
-- Name: documents_documentfolder_files id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.documents_documentfolder_files ALTER COLUMN id SET DEFAULT nextval('public.documents_documentfolder_files_id_seq'::regclass);


--
-- Name: library_cache id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.library_cache ALTER COLUMN id SET DEFAULT nextval('public.library_cache_id_seq'::regclass);


--
-- Name: library_folder id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.library_folder ALTER COLUMN id SET DEFAULT nextval('public.library_folder_id_seq'::regclass);


--
-- Name: library_folder_children id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.library_folder_children ALTER COLUMN id SET DEFAULT nextval('public.library_folder_children_id_seq'::regclass);


--
-- Name: library_folder_lesson_list id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.library_folder_lesson_list ALTER COLUMN id SET DEFAULT nextval('public.library_folder_lesson_list_id_seq'::regclass);


--
-- Name: news_post id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.news_post ALTER COLUMN id SET DEFAULT nextval('public.news_post_id_seq'::regclass);


--
-- Name: papers_comment id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_comment ALTER COLUMN id SET DEFAULT nextval('public.papers_comment_id_seq'::regclass);


--
-- Name: papers_comment_dislikes id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_comment_dislikes ALTER COLUMN id SET DEFAULT nextval('public.papers_comment_dislikes_id_seq'::regclass);


--
-- Name: papers_comment_likes id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_comment_likes ALTER COLUMN id SET DEFAULT nextval('public.papers_comment_likes_id_seq'::regclass);


--
-- Name: papers_course id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_course ALTER COLUMN id SET DEFAULT nextval('public.papers_course_id_seq'::regclass);


--
-- Name: papers_course_done_by id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_course_done_by ALTER COLUMN id SET DEFAULT nextval('public.papers_course_done_by_id_seq'::regclass);


--
-- Name: papers_course_lessons id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_course_lessons ALTER COLUMN id SET DEFAULT nextval('public.papers_course_lesson_id_seq'::regclass);


--
-- Name: papers_course_students id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_course_students ALTER COLUMN id SET DEFAULT nextval('public.papers_course_students_id_seq'::regclass);


--
-- Name: papers_lesson id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_lesson ALTER COLUMN id SET DEFAULT nextval('public.papers_lesson_id_seq'::regclass);


--
-- Name: papers_lesson_done_by id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_lesson_done_by ALTER COLUMN id SET DEFAULT nextval('public.papers_lesson_done_by_id_seq'::regclass);


--
-- Name: papers_lesson_papers id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_lesson_papers ALTER COLUMN id SET DEFAULT nextval('public.papers_lesson_papers_id_seq'::regclass);


--
-- Name: papers_paper id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_paper ALTER COLUMN id SET DEFAULT nextval('public.papers_paper_id_seq'::regclass);


--
-- Name: papers_paper_done_by id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_paper_done_by ALTER COLUMN id SET DEFAULT nextval('public.papers_paper_done_by_id_seq'::regclass);


--
-- Name: papers_paper_subthemes id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_paper_subthemes ALTER COLUMN id SET DEFAULT nextval('public.papers_paper_subthemes_id_seq'::regclass);


--
-- Name: papers_subtheme id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_subtheme ALTER COLUMN id SET DEFAULT nextval('public.papers_subtheme_id_seq'::regclass);


--
-- Name: papers_subtheme_task_list id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_subtheme_task_list ALTER COLUMN id SET DEFAULT nextval('public.papers_subtheme_task_list_id_seq'::regclass);


--
-- Name: schools_cabinet id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schools_cabinet ALTER COLUMN id SET DEFAULT nextval('public.schools_cabinett_id_seq'::regclass);


--
-- Name: schools_office id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schools_office ALTER COLUMN id SET DEFAULT nextval('public.schools_office_id_seq'::regclass);


--
-- Name: schools_school id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schools_school ALTER COLUMN id SET DEFAULT nextval('public.schools_school_id_seq'::regclass);


--
-- Name: schools_subjectage id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schools_subjectage ALTER COLUMN id SET DEFAULT nextval('public.schools_subjectage_id_seq'::regclass);


--
-- Name: schools_subjectcategory id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schools_subjectcategory ALTER COLUMN id SET DEFAULT nextval('public.schools_subjectcategory_id_seq'::regclass);


--
-- Name: squads_squad id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.squads_squad ALTER COLUMN id SET DEFAULT nextval('public.squads_squad_id_seq'::regclass);


--
-- Name: squads_squad_curator id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.squads_squad_curator ALTER COLUMN id SET DEFAULT nextval('public.squads_squad_curator_id_seq'::regclass);


--
-- Name: squads_squad_students id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.squads_squad_students ALTER COLUMN id SET DEFAULT nextval('public.squads_squad_students_id_seq'::regclass);


--
-- Name: subjects_attendance id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_attendance ALTER COLUMN id SET DEFAULT nextval('public.subjects_attendance_id_seq'::regclass);


--
-- Name: subjects_cacheattendance id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_cacheattendance ALTER COLUMN id SET DEFAULT nextval('public.subjects_cacheattendance_id_seq'::regclass);


--
-- Name: subjects_cell id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_cell ALTER COLUMN id SET DEFAULT nextval('public.subjects_cell_id_seq'::regclass);


--
-- Name: subjects_day id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_day ALTER COLUMN id SET DEFAULT nextval('public.subjects_day_id_seq'::regclass);


--
-- Name: subjects_lecture id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_lecture ALTER COLUMN id SET DEFAULT nextval('public.subjects_lecture_id_seq'::regclass);


--
-- Name: subjects_lecture_people id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_lecture_people ALTER COLUMN id SET DEFAULT nextval('public.subjects_lecture_people_id_seq'::regclass);


--
-- Name: subjects_subject id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subject ALTER COLUMN id SET DEFAULT nextval('public.subjects_subject_id_seq'::regclass);


--
-- Name: subjects_subject_squads id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subject_squads ALTER COLUMN id SET DEFAULT nextval('public.subjects_subject_squads_id_seq'::regclass);


--
-- Name: subjects_subject_students id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subject_students ALTER COLUMN id SET DEFAULT nextval('public.subjects_subject_students_id_seq'::regclass);


--
-- Name: subjects_subject_teacher id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subject_teacher ALTER COLUMN id SET DEFAULT nextval('public.subjects_subject_teacher_id_seq'::regclass);


--
-- Name: subjects_subjectmaterials id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subjectmaterials ALTER COLUMN id SET DEFAULT nextval('public.subjects_subjectmaterials_id_seq'::regclass);


--
-- Name: subjects_subjectmaterials_done_by id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subjectmaterials_done_by ALTER COLUMN id SET DEFAULT nextval('public.subjects_subjectmaterials_done_by_id_seq'::regclass);


--
-- Name: subjects_subjectmaterials_lessons id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subjectmaterials_lessons ALTER COLUMN id SET DEFAULT nextval('public.subjects_subjectmaterials_lessons_id_seq'::regclass);


--
-- Name: subjects_timeperiod id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_timeperiod ALTER COLUMN id SET DEFAULT nextval('public.subjects_timeperiod_id_seq'::regclass);


--
-- Name: subjects_timeperiod_people id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_timeperiod_people ALTER COLUMN id SET DEFAULT nextval('public.subjects_timeperiod_students_id_seq'::regclass);


--
-- Name: tasks_problemtag id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks_problemtag ALTER COLUMN id SET DEFAULT nextval('public.tasks_problemtag_id_seq'::regclass);


--
-- Name: tasks_solver id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks_solver ALTER COLUMN id SET DEFAULT nextval('public.tasks_solver_id_seq'::regclass);


--
-- Name: tasks_task id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks_task ALTER COLUMN id SET DEFAULT nextval('public.tasks_task_id_seq'::regclass);


--
-- Name: tasks_task_tags id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks_task_tags ALTER COLUMN id SET DEFAULT nextval('public.tasks_task_tags_id_seq'::regclass);


--
-- Name: todolist_board id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_board ALTER COLUMN id SET DEFAULT nextval('public.todolist_board_id_seq'::regclass);


--
-- Name: todolist_card id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_card ALTER COLUMN id SET DEFAULT nextval('public.todolist_card_id_seq'::regclass);


--
-- Name: todolist_card_doc_list id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_card_doc_list ALTER COLUMN id SET DEFAULT nextval('public.todolist_card_doc_list_id_seq'::regclass);


--
-- Name: todolist_card_metka_list id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_card_metka_list ALTER COLUMN id SET DEFAULT nextval('public.todolist_card_metka_list_id_seq'::regclass);


--
-- Name: todolist_card_user_list id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_card_user_list ALTER COLUMN id SET DEFAULT nextval('public.todolist_card_user_list_id_seq'::regclass);


--
-- Name: todolist_column id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_column ALTER COLUMN id SET DEFAULT nextval('public.todolist_column_id_seq'::regclass);


--
-- Name: todolist_comment id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_comment ALTER COLUMN id SET DEFAULT nextval('public.todolist_comment_id_seq'::regclass);


--
-- Name: todolist_comment_ffile id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_comment_ffile ALTER COLUMN id SET DEFAULT nextval('public.todolist_comment_ffile_id_seq'::regclass);


--
-- Name: todolist_document id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_document ALTER COLUMN id SET DEFAULT nextval('public.todolist_document_id_seq'::regclass);


--
-- Name: todolist_metka id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_metka ALTER COLUMN id SET DEFAULT nextval('public.todolist_metka_id_seq'::regclass);


--
-- Data for Name: accounts_corruption; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.accounts_corruption (id, text, author_profile_id, school_id) FROM stdin;
\.


--
-- Data for Name: accounts_crmcard; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.accounts_crmcard (id, name, phone, mail, comments, "timestamp", author_profile_id, column_id, school_id, saved) FROM stdin;
2	Qwerty qwertyuuio	+7(702)389-74-62	mailamialmlai	mmm	2019-04-07 20:25:37.671438+06	119	4	1	t
4	Иван Иванов	+77023897462	123213213	4	2019-04-08 20:13:26.913619+06	\N	2	1	f
1	Иван Иванов	+77023897462	123213213	4	2019-04-07 17:24:44.296819+06	119	4	1	t
3	ASdfgh WSEDFRG	+7(702)389-74-62	mailamialmlai	w	2019-04-07 20:50:08.813745+06	119	4	1	t
5	new1	2	2	2	2019-04-08 20:15:11.269566+06	\N	4	1	f
7	new3	new	\\894\n5	n	2019-04-08 20:17:09.008012+06	\N	2	1	f
6	qwe	qwe	qwe	qwe	2019-04-08 20:15:25.814097+06	\N	4	1	f
8	xxx	x	x	x	2019-04-10 06:07:04.800235+06	\N	2	1	f
\.


--
-- Data for Name: accounts_crmcolumn; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.accounts_crmcolumn (id, title, number_of_cards, school_id) FROM stdin;
3	Посетители пробное занятие	53	1
4	Купили абонемент	48	1
1	Заявка на сайте	12	1
2	Записались на пробное занятие	21	1
\.


--
-- Data for Name: accounts_jobcategory; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.accounts_jobcategory (id, title, salary, profession_id) FROM stdin;
1	Младший тренер	500	1
2	Старший тренер	7000	1
\.


--
-- Data for Name: accounts_misslesson; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.accounts_misslesson (id, text, image, height_field, width_field, dates, profile_id) FROM stdin;
20	ok		0	0	{2019-03-15,2019-03-13,2019-03-07,2019-03-14,2019-03-06,2019-04-11,2019-04-10}	119
\.


--
-- Data for Name: accounts_profession; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.accounts_profession (id, title) FROM stdin;
1	Teacher
2	Manager
3	Director
4	CEO
5	Creator
6	Admin
7	Moderator
8	Student
\.


--
-- Data for Name: accounts_profile; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.accounts_profile (id, coins, birthdate, first_name, phone, image, height_field, width_field, mail, user_id, easy_skills, tag_ids, hard_skills, middle_skills, pro_skills, money, crm_age_id, crm_office_id, crm_subject_id, is_student, hint) FROM stdin;
120	19600	2019-02-15	uuuuuuu	u	Снимок_экрана_от_2018-09-22_00-06-11.png	556	765	u	95	{1,2}	{1,2}	{1,2}	{1,2}	{1,2}	0	1	1	1	t	0
121	0	\N	mko	777		0	0	777	96	{}	{}	{}	{}	{}	0	\N	\N	\N	t	0
124	0	\N	mrt	555		0	0	55	99	{}	{}	{}	{}	{}	0	\N	\N	\N	t	0
125	0	\N	njnjde	njnj		0	0	njn	100	{}	{}	{}	{}	{}	0	\N	\N	\N	t	0
122	0	\N	qwe	qwe		0	0	qqwe	97	{}	{}	{}	{}	{}	0	\N	\N	\N	t	0
128	0	2019-04-05	erg	rfe`f`	dark.png	602	1070	ertv	103	{1,2}	{1,2}	{1,2}	{1,2}	{1,2}	0	1	1	1	t	0
127	0	\N	x1	x1		0	0	zz1	102	{}	{}	{}	{}	{}	0	\N	\N	\N	t	0
126	0	\N	xxx2	x2		0	0	x2	101	{}	{}	{}	{}	{}	0	\N	\N	\N	t	0
123	0	\N	Турабек Альбина Ардаққызы	77777777777777		0	0	44444444	98	{}	{}	{}	{}	{}	0	\N	\N	\N	t	0
129	0	\N	jhuhuhuhu	uhbmbj		0	0	gjgy	104	{}	{}	{}	{}	{}	0	\N	\N	\N	t	0
130	0	\N	Test	123		0	0	testmail	105	{}	{}	{}	{}	{}	0	\N	\N	\N	t	0
135	0	\N	Qwerty qwertyuuio	+7(702)389-74-62		0	0	mailamialmlai	110	{}	{}	{}	{}	{}	0	\N	\N	\N	t	0
134	0	\N	Иван Иванов	+77023897462		0	0	123213213	109	{}	{}	{}	{}	{}	0	\N	\N	\N	t	0
131	0	\N	Test2	7744		0	0	test2	106	{}	{}	{}	{}	{}	0	\N	\N	\N	t	0
140	0	\N	Иван Иванов	+77023897462		0	0	123213213	115	{}	{}	{}	{}	{}	0	\N	\N	\N	t	0
132	0	\N	Test3	4774747		0	0	test3	107	{}	{}	{}	{}	{}	0	\N	\N	\N	t	0
136	0	\N	Qwerty qwertyuuio	+7(702)389-74-62		0	0	mailamialmlai	111	{}	{}	{}	{}	{}	0	\N	\N	\N	t	0
137	0	\N	ASdfgh WSEDFRG	+7(702)389-74-62		0	0	mailamialmlai	112	{}	{}	{}	{}	{}	0	\N	\N	\N	t	0
141	0	\N	ASdfgh WSEDFRG	+7(702)389-74-62		0	0	mailamialmlai	116	{}	{}	{}	{}	{}	0	\N	\N	\N	t	0
138	0	\N	qwe	qwe		0	0	qwe	113	{}	{}	{}	{}	{}	0	\N	\N	\N	t	0
139	0	\N	Qwerty qwertyuuio	+7(702)389-74-62		0	0	mailamialmlai	114	{}	{}	{}	{}	{}	0	\N	\N	\N	t	0
142	0	\N	Qwerty qwertyuuio	+7(702)389-74-62		0	0	mailamialmlai	117	{}	{}	{}	{}	{}	0	\N	\N	\N	t	0
119	999583	2019-02-14	admin	admin	photo_2019-01-19_10-26-04.jpg	640	640	admin	1	{1,2}	{1,2}	{1,2}	{1,2}	{1,2}	0	\N	\N	1	f	100
133	0	2019-04-07	Test4	8888	dark.png	602	1070	test4	108	{1,2}	{1,2}	{1,2}	{1,2}	{1,2}	0	1	1	1	f	100
\.


--
-- Data for Name: accounts_profile_job_categories; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.accounts_profile_job_categories (id, profile_id, jobcategory_id) FROM stdin;
1	119	1
2	120	1
3	128	1
4	133	1
\.


--
-- Data for Name: accounts_profile_profession; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.accounts_profile_profession (id, profile_id, profession_id) FROM stdin;
1	119	5
2	119	1
3	119	2
4	119	3
5	120	1
6	128	8
7	130	8
8	131	8
9	132	8
15	134	8
16	135	8
17	136	8
18	137	8
19	138	8
20	139	8
21	140	8
22	141	8
23	142	8
29	133	2
\.


--
-- Data for Name: accounts_profile_schools; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.accounts_profile_schools (id, profile_id, school_id) FROM stdin;
1	119	1
2	121	1
3	122	1
4	120	1
5	123	1
6	119	2
7	121	2
8	122	2
9	120	2
10	123	2
11	124	1
12	125	1
13	126	1
14	127	1
15	128	1
16	129	1
17	130	1
18	131	1
19	132	1
20	133	1
21	134	1
22	135	1
23	136	1
24	137	1
25	138	1
26	139	1
27	140	1
28	141	1
29	142	1
\.


--
-- Data for Name: accounts_zaiavka; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.accounts_zaiavka (id, first_name, phone, "timestamp", mail, school_id) FROM stdin;
1	nnnn	444	2019-02-16 16:46:49.286211+06	jhbehkgbejhrg	1
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add permission	2	add_permission
5	Can change permission	2	change_permission
6	Can delete permission	2	delete_permission
7	Can add group	3	add_group
8	Can change group	3	change_group
9	Can delete group	3	delete_group
10	Can add user	4	add_user
11	Can change user	4	change_user
12	Can delete user	4	delete_user
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add main page	7	add_mainpage
20	Can change main page	7	change_mainpage
21	Can delete main page	7	delete_mainpage
22	Can add profile	8	add_profile
23	Can change profile	8	change_profile
24	Can delete profile	8	delete_profile
25	Can add zaiavka	9	add_zaiavka
26	Can change zaiavka	9	change_zaiavka
27	Can delete zaiavka	9	delete_zaiavka
28	Can add corruption	10	add_corruption
29	Can change corruption	10	change_corruption
30	Can delete corruption	10	delete_corruption
31	Can add profile schedule cell	11	add_profileschedulecell
32	Can change profile schedule cell	11	change_profileschedulecell
33	Can delete profile schedule cell	11	delete_profileschedulecell
34	Can add follow	12	add_follow
35	Can change follow	12	change_follow
36	Can delete follow	12	delete_follow
37	Can add squad	13	add_squad
38	Can change squad	13	change_squad
39	Can delete squad	13	delete_squad
40	Can add squad category	14	add_squadcategory
41	Can change squad category	14	change_squadcategory
42	Can delete squad category	14	delete_squadcategory
43	Can add squad week	15	add_squadweek
44	Can change squad week	15	change_squadweek
45	Can delete squad week	15	delete_squadweek
46	Can add lesson	16	add_lesson
47	Can change lesson	16	change_lesson
48	Can delete lesson	16	delete_lesson
49	Can add paper	17	add_paper
50	Can change paper	17	change_paper
51	Can delete paper	17	delete_paper
52	Can add subtheme	18	add_subtheme
53	Can change subtheme	18	change_subtheme
54	Can delete subtheme	18	delete_subtheme
55	Can add comment	19	add_comment
56	Can change comment	19	change_comment
57	Can delete comment	19	delete_comment
58	Can add course	20	add_course
59	Can change course	20	change_course
60	Can delete course	20	delete_course
61	Can add solver	21	add_solver
62	Can change solver	21	change_solver
63	Can delete solver	21	delete_solver
64	Can add task	22	add_task
65	Can change task	22	change_task
66	Can delete task	22	delete_task
67	Can add problem tag	23	add_problemtag
68	Can change problem tag	23	change_problemtag
69	Can delete problem tag	23	delete_problemtag
70	Can add board	24	add_board
71	Can change board	24	change_board
72	Can delete board	24	delete_board
73	Can add card	25	add_card
74	Can change card	25	change_card
75	Can delete card	25	delete_card
76	Can add column	26	add_column
77	Can change column	26	change_column
78	Can delete column	26	delete_column
79	Can add comment	27	add_comment
80	Can change comment	27	change_comment
81	Can delete comment	27	delete_comment
82	Can add document	28	add_document
83	Can change document	28	change_document
84	Can delete document	28	delete_document
85	Can add metka	29	add_metka
86	Can change metka	29	change_metka
87	Can delete metka	29	delete_metka
88	Can add cache	30	add_cache
89	Can change cache	30	change_cache
90	Can delete cache	30	delete_cache
91	Can add folder	31	add_folder
92	Can change folder	31	change_folder
93	Can delete folder	31	delete_folder
94	Can add course folder	32	add_coursefolder
95	Can change course folder	32	change_coursefolder
96	Can delete course folder	32	delete_coursefolder
97	Can add cell	33	add_cell
98	Can change cell	33	change_cell
99	Can delete cell	33	delete_cell
100	Can add day	34	add_day
101	Can change day	34	change_day
102	Can delete day	34	delete_day
103	Can add lecture	35	add_lecture
104	Can change lecture	35	change_lecture
105	Can delete lecture	35	delete_lecture
106	Can add subject	36	add_subject
107	Can change subject	36	change_subject
108	Can delete subject	36	delete_subject
109	Can add subject category	37	add_subjectcategory
110	Can change subject category	37	change_subjectcategory
111	Can delete subject category	37	delete_subjectcategory
112	Can add time period	38	add_timeperiod
113	Can change time period	38	change_timeperiod
114	Can delete time period	38	delete_timeperiod
115	Can add subject materials	39	add_subjectmaterials
116	Can change subject materials	39	change_subjectmaterials
117	Can delete subject materials	39	delete_subjectmaterials
118	Can add squad cell	40	add_squadcell
119	Can change squad cell	40	change_squadcell
120	Can delete squad cell	40	delete_squadcell
121	Can add attendance	41	add_attendance
122	Can change attendance	41	change_attendance
123	Can delete attendance	41	delete_attendance
124	Can add post	42	add_post
125	Can change post	42	change_post
126	Can delete post	42	delete_post
127	Can add school	43	add_school
128	Can change school	43	change_school
129	Can delete school	43	delete_school
130	Can add document cache	44	add_documentcache
131	Can change document cache	44	change_documentcache
132	Can delete document cache	44	delete_documentcache
133	Can add document folder	45	add_documentfolder
134	Can change document folder	45	change_documentfolder
135	Can delete document folder	45	delete_documentfolder
175	Can view log entry	1	view_logentry
176	Can view permission	2	view_permission
177	Can view group	3	view_group
178	Can view user	4	view_user
179	Can view content type	5	view_contenttype
180	Can view session	6	view_session
181	Can view main page	7	view_mainpage
182	Can view profile	8	view_profile
183	Can view zaiavka	9	view_zaiavka
184	Can view corruption	10	view_corruption
185	Can view profile schedule cell	11	view_profileschedulecell
186	Can view follow	12	view_follow
187	Can view squad	13	view_squad
188	Can view squad category	14	view_squadcategory
189	Can view squad week	15	view_squadweek
190	Can view lesson	16	view_lesson
191	Can view paper	17	view_paper
192	Can view subtheme	18	view_subtheme
193	Can view comment	19	view_comment
194	Can view course	20	view_course
195	Can view solver	21	view_solver
196	Can view task	22	view_task
197	Can view problem tag	23	view_problemtag
198	Can view board	24	view_board
199	Can view card	25	view_card
200	Can view column	26	view_column
201	Can view comment	27	view_comment
202	Can view document	28	view_document
203	Can view metka	29	view_metka
204	Can view cache	30	view_cache
205	Can view folder	31	view_folder
206	Can view course folder	32	view_coursefolder
207	Can view cell	33	view_cell
208	Can view day	34	view_day
209	Can view lecture	35	view_lecture
210	Can view subject	36	view_subject
211	Can view subject category	37	view_subjectcategory
212	Can view time period	38	view_timeperiod
213	Can view subject materials	39	view_subjectmaterials
214	Can view squad cell	40	view_squadcell
215	Can view attendance	41	view_attendance
216	Can view post	42	view_post
217	Can view school	43	view_school
218	Can view document cache	44	view_documentcache
219	Can view document folder	45	view_documentfolder
220	Can add job category	58	add_jobcategory
221	Can change job category	58	change_jobcategory
222	Can delete job category	58	delete_jobcategory
223	Can view job category	58	view_jobcategory
224	Can add profession	59	add_profession
225	Can change profession	59	change_profession
226	Can delete profession	59	delete_profession
227	Can view profession	59	view_profession
228	Can add cabinet	60	add_cabinet
229	Can change cabinet	60	change_cabinet
230	Can delete cabinet	60	delete_cabinet
231	Can view cabinet	60	view_cabinet
232	Can add cabinett	63	add_cabinett
233	Can change cabinett	63	change_cabinett
234	Can delete cabinett	63	delete_cabinett
235	Can view cabinett	63	view_cabinett
236	Can add subject age	61	add_subjectage
237	Can change subject age	61	change_subjectage
238	Can delete subject age	61	delete_subjectage
239	Can view subject age	61	view_subjectage
240	Can add subject category	62	add_subjectcategory
241	Can change subject category	62	change_subjectcategory
242	Can delete subject category	62	delete_subjectcategory
243	Can view subject category	62	view_subjectcategory
244	Can add office	64	add_office
245	Can change office	64	change_office
246	Can delete office	64	delete_office
247	Can view office	64	view_office
248	Can add miss lesson	65	add_misslesson
249	Can change miss lesson	65	change_misslesson
250	Can delete miss lesson	65	delete_misslesson
251	Can view miss lesson	65	view_misslesson
252	Can add cache attendance	66	add_cacheattendance
253	Can change cache attendance	66	change_cacheattendance
254	Can delete cache attendance	66	delete_cacheattendance
255	Can view cache attendance	66	view_cacheattendance
256	Can add crm card	67	add_crmcard
257	Can change crm card	67	change_crmcard
258	Can delete crm card	67	delete_crmcard
259	Can view crm card	67	view_crmcard
260	Can add crm column	68	add_crmcolumn
261	Can change crm column	68	change_crmcolumn
262	Can delete crm column	68	delete_crmcolumn
263	Can view crm column	68	view_crmcolumn
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
111	!dSoUtMHkzfnLnNOoHcBwolOPoTJLAXqqSAaiNiTk	\N	f	user111				f	t	2019-04-10 05:38:35.513551+06
96	pbkdf2_sha256$120000$l8caWTUrJurM$w610AWDANKLSL6xnMyTsERfaFBCvd3wlumMwCSOxddg=	\N	f	user96				f	t	2019-02-16 09:26:58.073476+06
97	pbkdf2_sha256$120000$GcxrT6nnJFKY$3XXqnO52lcQkWcHgy1F51+Wq1uQns3xYNymYzikiKQ8=	\N	f	user97				f	t	2019-02-16 09:27:05.76295+06
98	pbkdf2_sha256$120000$suRRhAAm997i$ZvXjPbvt+pi/zUIuXWtsd9nRQFyMFT7S9ivvc/9/URw=	\N	f	user98				f	t	2019-02-16 18:26:50.252113+06
112	!ON6R68LifxLt5IPKXbA7GPf99c8OPZwX9a5An1jH	\N	f	user112				f	t	2019-04-10 05:38:51.377158+06
99	pbkdf2_sha256$120000$EQua1YTXF2Yo$P8Hs811gqyoEkm+UEGiCBY9GD30tiXM195AMjoZns0g=	\N	f	user99				f	t	2019-02-19 04:40:52.748998+06
113	!ozkvkiEH67x2VMcLxemyEw4qtRb1UXsbm4qlvwWh	\N	f	user113				f	t	2019-04-10 05:39:10.602615+06
100	pbkdf2_sha256$120000$AiQw3Pmr6kV8$yWs+f/n4IojPq2Z1kCfVHg50rm7AkEdtginrdvxnZKg=	2019-03-02 07:46:42.392862+06	f	user100				f	t	2019-03-02 07:39:08.55851+06
101	pbkdf2_sha256$120000$1bQNQwshMPsW$40ABf/UEvWWpfFy7AvQFLENkbP0GCQ4Y0Gdfv6CaZSc=	\N	f	user101				f	t	2019-03-02 07:48:09.073535+06
102	pbkdf2_sha256$120000$iasrJswlfVRY$SOpjcbnMP2ms7hD/u/dIxc2iY0LVxnIBB7BBSSQ9wRo=	\N	f	user102				f	t	2019-03-02 07:49:01.384801+06
103	pbkdf2_sha256$120000$DwupG5Dbf14n$i2LGmGz9oQyyvMv8hDwtSYRxUC1I4RbYYuLBWpdtPpw=	\N	f	user103				f	t	2019-03-03 18:21:45.682403+06
114	!lSwev8RnxS0HfSbapmaBgIQXvcdpbKkcKTinxHWH	\N	f	user114				f	t	2019-04-10 05:41:39.444237+06
115	!KGRLzMtKTelvW7CJqrCrdgfWchju6opghZnJU8vl	\N	f	user115				f	t	2019-04-10 05:46:47.150179+06
104	pbkdf2_sha256$120000$GQP6RvyhHH79$zfp8yG0W0jTuoWAhVkYGjf0cK12uiMwy0tRdg0C+l3g=	\N	f	user104				f	t	2019-04-01 17:19:40.092312+06
95	pbkdf2_sha256$120000$wwk70DyW3RLf$suKQWWfPy1KFqH8BYsdIwBX7Jltf3BuWILvTRU1T5vI=	2019-04-04 19:02:11.631048+06	f	u				f	t	2019-02-15 03:21:53.534151+06
116	!9XGI9SegLyNjKjapSd8jJa7vCZ2ZLnuAVYmHokQY	\N	f	user116				f	t	2019-04-10 05:58:21.185354+06
117	!2yiIK2RU6axQ6jB98BItazuvVjhWmNH6zNKyRJvs	\N	f	user117				f	t	2019-04-10 05:59:33.572128+06
108	pbkdf2_sha256$120000$QqeiKpoBJk2o$5xiEcEmw1N/WJj59KNr9BPo/+dWgjAbFiTAIBgaLmyw=	2019-04-10 11:00:01.642121+06	f	user108				f	t	2019-04-07 12:28:12.189118+06
105	pbkdf2_sha256$120000$SvWZOFsH0kFB$XdF+zNYUiBzMs/Ssihi7tun7liV2rYqDKmyNpmBuA08=	2019-04-05 21:09:38.575577+06	f	user105				f	t	2019-04-05 14:53:16.91265+06
1	pbkdf2_sha256$120000$uSeSVj9ANc86$OZIT+mU+jAuNk8BCHrpPan+0W2PiWduA4SXKUd6Wej4=	2019-04-14 17:55:13.212995+06	t	admin			admin@mail.com	t	t	2019-02-14 16:54:28.747875+06
106	pbkdf2_sha256$120000$H5e195zGie99$2X0BcPkcDf2GTqsvixz3K9Oy9SoF746dWte2DmVEN+Q=	2019-04-06 12:12:11.119412+06	f	user106				f	t	2019-04-06 12:11:26.454055+06
107	pbkdf2_sha256$120000$ZDVGbaWqev4A$pRpKXjQDpQDwjePbQaZnSBXwyc6XTwyDrvp8obHd4rQ=	2019-04-06 12:19:14.82052+06	f	user107				f	t	2019-04-06 12:18:20.587602+06
109	!1X5DkEi4FCp9KXCfw7o5aOul7lgI42nP70Hu4MhS	\N	f	user109				f	t	2019-04-09 13:46:35.121264+06
110	!3muEhBfKO6AwWYSOqEAFzYqcMCxlRAHZnLNgmhsu	\N	f	user110				f	t	2019-04-10 05:38:29.675145+06
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2019-02-14 18:09:13.398136+06	1	School object (1)	1	[{"added": {}}]	43	1
2	2019-02-14 18:09:18.109257+06	2	School object (2)	1	[{"added": {}}]	43	1
3	2019-02-14 18:09:18.516154+06	3	School object (3)	1	[{"added": {}}]	43	1
4	2019-02-14 20:38:16.439404+06	1	Profile object (1)	3		8	1
5	2019-02-14 20:38:28.748102+06	3	School object (3)	3		43	1
6	2019-02-14 20:38:28.763435+06	2	School object (2)	3		43	1
7	2019-02-14 20:38:28.774472+06	1	School object (1)	3		43	1
1668	2019-02-14 20:41:51.500201+06	119	Profile object (119)	1	[{"added": {}}]	8	1
1669	2019-02-14 21:06:49.578156+06	119	Profile object (119)	2	[{"changed": {"fields": ["hisschedule"]}}]	8	1
1670	2019-02-15 03:21:53.658009+06	95	u	1	[{"added": {}}]	4	1
1671	2019-02-15 03:22:48.607408+06	120	Profile object (120)	2	[{"changed": {"fields": ["first_name", "school", "birthdate", "mail", "phone", "image", "tag_ids", "easy_skills", "middle_skills", "hard_skills", "pro_skills", "hisschedule"]}}]	8	1
1672	2019-02-16 09:07:37.413063+06	119	Profile object (119)	2	[{"changed": {"fields": ["is_director"]}}]	8	1
1673	2019-02-16 09:07:39.245334+06	119	Profile object (119)	2	[]	8	1
1674	2019-02-16 09:08:15.291998+06	119	Profile object (119)	2	[{"changed": {"fields": ["is_director"]}}]	8	1
1675	2019-02-16 16:46:49.28739+06	1	Zaiavka object (1)	1	[{"added": {}}]	9	1
1676	2019-02-16 17:31:57.92132+06	1	Zaiavka object (1)	2	[{"changed": {"fields": ["mail"]}}]	9	1
1677	2019-02-23 22:20:17.424981+06	1	Profession object (1)	1	[{"added": {}}]	59	1
1678	2019-02-23 22:20:23.365901+06	2	Profession object (2)	1	[{"added": {}}]	59	1
1679	2019-02-23 22:20:30.380282+06	3	Profession object (3)	1	[{"added": {}}]	59	1
1680	2019-02-23 22:20:40.748891+06	3	Profession object (3)	2	[{"changed": {"fields": ["title"]}}]	59	1
1681	2019-02-23 22:20:50.264971+06	4	Profession object (4)	1	[{"added": {}}]	59	1
1682	2019-02-23 22:20:57.727419+06	5	Profession object (5)	1	[{"added": {}}]	59	1
1683	2019-02-23 22:21:03.346943+06	6	Profession object (6)	1	[{"added": {}}]	59	1
1684	2019-02-23 22:21:13.916272+06	7	Profession object (7)	1	[{"added": {}}]	59	1
1685	2019-02-23 22:27:24.960546+06	1	JobCategory object (1)	1	[{"added": {}}]	58	1
1686	2019-02-23 22:35:06.747564+06	119	Profile object (119)	2	[{"changed": {"fields": ["profession", "job_categories"]}}]	8	1
1687	2019-02-23 22:36:14.90077+06	119	Profile object (119)	2	[{"changed": {"fields": ["profession"]}}]	8	1
1688	2019-02-26 06:39:32.759211+06	1	TimePeriod object (1)	2	[{"changed": {"fields": ["people"]}}]	38	1
1689	2019-02-26 06:39:42.851142+06	2	TimePeriod object (2)	2	[{"changed": {"fields": ["people"]}}]	38	1
1690	2019-02-26 06:39:51.650917+06	3	TimePeriod object (3)	2	[{"changed": {"fields": ["people"]}}]	38	1
1691	2019-02-26 06:41:13.527346+06	8	Profession object (8)	1	[{"added": {}}]	59	1
1692	2019-02-27 06:07:08.514157+06	1	SubjectAge object (1)	1	[{"added": {}}]	61	1
1693	2019-02-27 06:07:19.685946+06	1	SubjectCategory object (1)	1	[{"added": {}}]	62	1
1694	2019-02-27 06:20:38.28358+06	1	Cabinett object (1)	1	[{"added": {}}]	63	1
1695	2019-02-27 06:40:11.815552+06	2	Cabinett object (2)	1	[{"added": {}}]	63	1
1696	2019-02-27 06:40:44.098958+06	3	Cabinett object (3)	1	[{"added": {}}]	63	1
1697	2019-02-27 06:41:36.001728+06	4	Cabinett object (4)	1	[{"added": {}}]	63	1
1698	2019-02-27 06:57:14.365973+06	2	SubjectCategory object (2)	1	[{"added": {}}]	62	1
1699	2019-02-27 22:55:16.802557+06	1	Office object (1)	1	[{"added": {}}]	64	1
1700	2019-02-28 08:09:32.544056+06	1	TimePeriod object (1)	2	[{"changed": {"fields": ["start"]}}]	38	1
1701	2019-02-28 11:41:43.741146+06	9	Subject object (9)	2	[{"changed": {"fields": ["image_icon", "category", "image_banner", "image_back", "slogan"]}}]	36	1
1702	2019-03-07 18:37:46.971753+06	10	MissLesson object (10)	3		65	1
1703	2019-03-07 18:37:47.015371+06	9	MissLesson object (9)	3		65	1
1704	2019-03-07 18:37:47.026444+06	8	MissLesson object (8)	3		65	1
1705	2019-03-07 18:37:47.037495+06	7	MissLesson object (7)	3		65	1
1706	2019-03-07 18:37:47.04868+06	6	MissLesson object (6)	3		65	1
1707	2019-03-07 18:37:47.059741+06	5	MissLesson object (5)	3		65	1
1708	2019-03-07 18:37:47.07096+06	4	MissLesson object (4)	3		65	1
1709	2019-03-07 18:37:47.082009+06	3	MissLesson object (3)	3		65	1
1710	2019-03-07 18:37:47.092991+06	2	MissLesson object (2)	3		65	1
1711	2019-03-07 18:37:47.104118+06	1	MissLesson object (1)	3		65	1
1712	2019-03-07 19:24:50.83253+06	19	MissLesson object (19)	3		65	1
1713	2019-03-07 19:24:50.852747+06	18	MissLesson object (18)	3		65	1
1714	2019-03-07 19:24:50.863625+06	17	MissLesson object (17)	3		65	1
1715	2019-03-07 19:24:50.874728+06	16	MissLesson object (16)	3		65	1
1716	2019-03-07 19:24:50.886127+06	15	MissLesson object (15)	3		65	1
1717	2019-03-07 19:24:50.897162+06	14	MissLesson object (14)	3		65	1
1718	2019-03-07 19:24:50.908281+06	13	MissLesson object (13)	3		65	1
1719	2019-03-07 19:24:50.919146+06	12	MissLesson object (12)	3		65	1
1720	2019-03-07 19:24:50.930484+06	11	MissLesson object (11)	3		65	1
1721	2019-03-12 18:56:19.477631+06	119	Profile object (119)	2	[{"changed": {"fields": ["is_student", "crm_office"]}}]	8	1
1722	2019-04-01 17:24:38.273566+06	120	Profile object (120)	2	[{"changed": {"fields": ["profession", "job_categories", "coins", "crm_subject", "crm_age", "crm_office"]}}]	8	1
1723	2019-04-05 14:49:37.06985+06	128	Profile object (128)	2	[{"changed": {"fields": ["profession", "job_categories", "birthdate", "image", "tag_ids", "easy_skills", "middle_skills", "hard_skills", "pro_skills", "crm_subject", "crm_age", "crm_office"]}}]	8	1
1724	2019-04-07 17:19:39.76203+06	1	CRMColumn object (1)	1	[{"added": {}}]	68	1
1725	2019-04-07 17:20:05.684723+06	2	CRMColumn object (2)	1	[{"added": {}}]	68	1
1726	2019-04-07 17:20:17.774265+06	3	CRMColumn object (3)	1	[{"added": {}}]	68	1
1727	2019-04-07 17:20:28.870972+06	4	CRMColumn object (4)	1	[{"added": {}}]	68	1
1728	2019-04-07 17:24:44.298178+06	1	CRMCard object (1)	1	[{"added": {}}]	67	1
1729	2019-04-07 19:08:15.028616+06	133	Profile object (133)	2	[{"changed": {"fields": ["profession", "job_categories", "is_student", "birthdate", "image", "tag_ids", "easy_skills", "middle_skills", "hard_skills", "pro_skills", "crm_subject", "crm_age", "crm_office"]}}]	8	1
1730	2019-04-07 19:09:37.326888+06	133	Profile object (133)	2	[{"changed": {"fields": ["profession"]}}]	8	1
1731	2019-04-07 19:10:28.486752+06	133	Profile object (133)	2	[{"changed": {"fields": ["profession"]}}]	8	1
1732	2019-04-07 19:10:58.796339+06	133	Profile object (133)	2	[{"changed": {"fields": ["profession"]}}]	8	1
1733	2019-04-07 20:25:37.672745+06	2	CRMCard object (2)	1	[{"added": {}}]	67	1
1734	2019-04-07 20:47:34.1392+06	1	CRMCard object (1)	2	[{"changed": {"fields": ["school"]}}]	67	1
1735	2019-04-07 20:47:40.655764+06	2	CRMCard object (2)	2	[{"changed": {"fields": ["school"]}}]	67	1
1736	2019-04-07 20:50:08.814736+06	3	CRMCard object (3)	1	[{"added": {}}]	67	1
1737	2019-04-10 03:45:37.035061+06	19	Subject object (19)	2	[{"changed": {"fields": ["image_icon", "office", "category", "age", "color_back", "content", "slogan"]}}]	36	1
1738	2019-04-10 03:46:07.283849+06	21	Subject object (21)	2	[{"changed": {"fields": ["office", "category", "age", "content", "slogan"]}}]	36	1
1739	2019-04-10 04:20:00.120574+06	22	Subject object (22)	2	[{"changed": {"fields": ["image_icon", "office", "category", "age", "image_banner", "image_back", "slogan"]}}]	36	1
1740	2019-04-10 04:40:49.937999+06	21	Subject object (21)	3		36	1
1741	2019-04-10 11:01:05.610528+06	133	Profile object (133)	2	[{"changed": {"fields": ["profession", "is_student"]}}]	8	1
1742	2019-04-10 11:14:15.952694+06	133	Profile object (133)	2	[{"changed": {"fields": ["profession", "is_student"]}}]	8	1
1743	2019-04-10 12:17:30.783404+06	133	Profile object (133)	2	[{"changed": {"fields": ["hint"]}}]	8	1
1744	2019-04-10 13:08:54.201934+06	133	Profile object (133)	2	[{"changed": {"fields": ["profession", "hint"]}}]	8	1
1745	2019-04-10 13:10:18.233235+06	133	Profile object (133)	2	[{"changed": {"fields": ["profession", "hint"]}}]	8	1
1746	2019-04-10 13:10:44.45483+06	133	Profile object (133)	2	[{"changed": {"fields": ["profession", "hint"]}}]	8	1
1747	2019-04-10 13:13:07.594867+06	133	Profile object (133)	2	[{"changed": {"fields": ["hint"]}}]	8	1
1748	2019-04-10 13:15:42.236212+06	133	Profile object (133)	2	[{"changed": {"fields": ["hint"]}}]	8	1
1749	2019-04-10 13:17:24.022027+06	133	Profile object (133)	2	[{"changed": {"fields": ["hint"]}}]	8	1
1750	2019-04-10 13:19:52.1121+06	133	Profile object (133)	2	[{"changed": {"fields": ["hint"]}}]	8	1
1751	2019-04-10 14:46:20.846986+06	133	Profile object (133)	2	[{"changed": {"fields": ["profession", "hint"]}}]	8	1
1752	2019-04-10 15:10:40.793497+06	133	Profile object (133)	2	[{"changed": {"fields": ["hint"]}}]	8	1
1753	2019-04-10 16:49:22.502945+06	133	Profile object (133)	2	[{"changed": {"fields": ["profession"]}}]	8	1
1754	2019-04-14 23:45:18.315721+06	2	JobCategory object (2)	1	[{"added": {}}]	58	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	accounts	mainpage
8	accounts	profile
9	accounts	zaiavka
10	accounts	corruption
11	accounts	profileschedulecell
12	squads	follow
13	squads	squad
14	squads	squadcategory
15	squads	squadweek
16	papers	lesson
17	papers	paper
18	papers	subtheme
19	papers	comment
20	papers	course
21	tasks	solver
22	tasks	task
23	tasks	problemtag
24	todolist	board
25	todolist	card
26	todolist	column
27	todolist	comment
28	todolist	document
29	todolist	metka
30	library	cache
31	library	folder
32	library	coursefolder
33	subjects	cell
34	subjects	day
35	subjects	lecture
36	subjects	subject
37	subjects	subjectcategory
38	subjects	timeperiod
39	subjects	subjectmaterials
40	subjects	squadcell
41	subjects	attendance
42	news	post
43	schools	school
44	documents	documentcache
45	documents	documentfolder
58	accounts	jobcategory
59	accounts	profession
60	schools	cabinet
61	schools	subjectage
62	schools	subjectcategory
63	schools	cabinett
64	schools	office
65	accounts	misslesson
66	subjects	cacheattendance
67	accounts	crmcard
68	accounts	crmcolumn
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2019-02-14 15:33:04.795161+06
2	auth	0001_initial	2019-02-14 15:33:05.631469+06
3	accounts	0001_initial	2019-02-14 15:33:06.602645+06
4	accounts	0002_profile_is_manager	2019-02-14 15:33:06.758723+06
5	accounts	0003_remove_profile_second_name	2019-02-14 15:33:06.791558+06
6	accounts	0004_profile_is_trener	2019-02-14 15:33:06.94791+06
7	accounts	0005_remove_profile_status	2019-02-14 15:33:06.980644+06
8	accounts	0006_auto_20181215_2030	2019-02-14 15:33:07.293257+06
9	accounts	0007_remove_profile_username	2019-02-14 15:33:07.326214+06
10	accounts	0008_auto_20181217_1451	2019-02-14 15:33:07.593802+06
11	accounts	0009_profile_is_ceo	2019-02-14 15:33:07.7493+06
12	accounts	0010_auto_20181217_1503	2019-02-14 15:33:07.905581+06
13	accounts	0011_auto_20181217_1505	2019-02-14 15:33:08.050535+06
14	accounts	0012_profile_school	2019-02-14 15:33:08.205956+06
15	schools	0001_initial	2019-02-14 15:33:08.462695+06
16	schools	0002_remove_school_curator	2019-02-14 15:33:08.496091+06
17	accounts	0013_auto_20190111_2030	2019-02-14 15:33:08.596141+06
18	accounts	0014_auto_20190111_2030	2019-02-14 15:33:08.75122+06
19	accounts	0015_auto_20190112_0119	2019-02-14 15:33:08.775895+06
20	accounts	0016_auto_20190112_0124	2019-02-14 15:33:08.801142+06
21	accounts	0017_auto_20190112_0126	2019-02-14 15:33:08.82099+06
22	accounts	0018_profile_is_director	2019-02-14 15:33:09.007937+06
23	accounts	0019_corruption	2019-02-14 15:33:09.185661+06
24	accounts	0020_auto_20190121_0735	2019-02-14 15:33:09.287071+06
25	accounts	0021_auto_20190121_1933	2019-02-14 15:33:09.306957+06
26	accounts	0022_auto_20190127_0121	2019-02-14 15:33:09.643166+06
27	accounts	0023_auto_20190127_0915	2019-02-14 15:33:10.144493+06
28	accounts	0024_profile_hisshedule	2019-02-14 15:33:10.33333+06
29	accounts	0025_auto_20190208_1122	2019-02-14 15:33:10.366408+06
30	accounts	0026_auto_20190208_1141	2019-02-14 15:33:10.399843+06
31	accounts	0027_auto_20190208_1143	2019-02-14 15:33:10.432827+06
32	accounts	0028_auto_20190208_1146	2019-02-14 15:33:10.499523+06
33	accounts	0029_auto_20190208_1150	2019-02-14 15:33:10.532929+06
34	accounts	0030_auto_20190208_1204	2019-02-14 15:33:10.56657+06
35	accounts	0031_auto_20190208_1226	2019-02-14 15:33:10.599672+06
36	accounts	0032_auto_20190208_1229	2019-02-14 15:33:10.633027+06
37	accounts	0033_auto_20190208_1236	2019-02-14 15:33:10.666225+06
38	accounts	0034_auto_20190209_2301	2019-02-14 15:33:10.933853+06
39	accounts	0035_auto_20190209_2308	2019-02-14 15:33:11.360321+06
40	accounts	0036_auto_20190209_2321	2019-02-14 15:33:11.470759+06
41	accounts	0037_auto_20190209_2352	2019-02-14 15:33:11.62682+06
42	admin	0001_initial	2019-02-14 15:33:11.838254+06
43	admin	0002_logentry_remove_auto_add	2019-02-14 15:33:11.860589+06
44	admin	0003_logentry_add_action_flag_choices	2019-02-14 15:33:11.884351+06
45	admin	0004_auto_20180927_1800	2019-02-14 15:33:11.904928+06
46	contenttypes	0002_remove_content_type_name	2019-02-14 15:33:11.949071+06
47	auth	0002_alter_permission_name_max_length	2019-02-14 15:33:11.971294+06
48	auth	0003_alter_user_email_max_length	2019-02-14 15:33:12.004941+06
49	auth	0004_alter_user_username_opts	2019-02-14 15:33:12.026807+06
50	auth	0005_alter_user_last_login_null	2019-02-14 15:33:12.060246+06
51	auth	0006_require_contenttypes_0002	2019-02-14 15:33:12.071754+06
52	auth	0007_alter_validators_add_error_messages	2019-02-14 15:33:12.096877+06
53	auth	0008_alter_user_username_max_length	2019-02-14 15:33:12.182977+06
54	auth	0009_alter_user_last_name_max_length	2019-02-14 15:33:12.216045+06
55	auth	0010_auto_20180927_1800	2019-02-14 15:33:12.405947+06
56	todolist	0001_initial	2019-02-14 15:33:13.686974+06
57	documents	0001_initial	2019-02-14 15:33:14.176663+06
58	documents	0002_auto_20190203_1201	2019-02-14 15:33:14.510288+06
59	tasks	0001_initial	2019-02-14 15:33:15.18999+06
60	papers	0001_initial	2019-02-14 15:33:16.114178+06
61	papers	0002_auto_20181125_0450	2019-02-14 15:33:16.154425+06
62	papers	0003_auto_20181129_0828	2019-02-14 15:33:16.425563+06
63	papers	0004_comment_parent	2019-02-14 15:33:16.525331+06
64	papers	0005_auto_20181129_1149	2019-02-14 15:33:16.564684+06
65	papers	0006_auto_20181129_1207	2019-02-14 15:33:16.97306+06
66	papers	0007_auto_20181129_1209	2019-02-14 15:33:17.384894+06
67	papers	0008_course	2019-02-14 15:33:18.086346+06
68	library	0001_initial	2019-02-14 15:33:18.766056+06
69	library	0002_folder_course_list	2019-02-14 15:33:18.986241+06
70	library	0003_auto_20181202_2044	2019-02-14 15:33:19.788262+06
71	library	0004_auto_20181224_1048	2019-02-14 15:33:19.841461+06
72	main	0001_initial	2019-02-14 15:33:19.943538+06
73	main	0002_delete_subject	2019-02-14 15:33:19.966413+06
74	news	0001_initial	2019-02-14 15:33:20.132911+06
75	news	0002_auto_20190204_0540	2019-02-14 15:33:20.288259+06
76	news	0003_auto_20190204_0543	2019-02-14 15:33:20.340998+06
77	papers	0009_course_cost	2019-02-14 15:33:20.511577+06
78	papers	0010_course_stars	2019-02-14 15:33:20.689703+06
79	papers	0011_course_students	2019-02-14 15:33:20.912176+06
80	papers	0012_auto_20181206_1035	2019-02-14 15:33:20.990021+06
81	papers	0013_paper_done_by	2019-02-14 15:33:21.234324+06
82	papers	0014_auto_20181231_1535	2019-02-14 15:33:21.513994+06
83	papers	0015_papersolver	2019-02-14 15:33:21.746727+06
84	papers	0016_lessonsolver	2019-02-14 15:33:21.924994+06
85	papers	0017_auto_20190109_2035	2019-02-14 15:33:22.582181+06
86	papers	0018_remove_subtheme_title	2019-02-14 15:33:22.625953+06
87	papers	0019_paper_typee	2019-02-14 15:33:22.937833+06
88	papers	0020_remove_paper_slug	2019-02-14 15:33:22.970974+06
89	papers	0021_auto_20190202_1232	2019-02-14 15:33:23.01502+06
90	papers	0022_auto_20190204_0829	2019-02-14 15:33:23.282575+06
91	papers	0023_lesson_estimaters	2019-02-14 15:33:23.4048+06
92	papers	0024_auto_20190204_0849	2019-02-14 15:33:23.794668+06
93	papers	0025_auto_20190207_0948	2019-02-14 15:33:23.835345+06
94	sessions	0001_initial	2019-02-14 15:33:24.038773+06
95	squads	0001_initial	2019-02-14 15:33:25.578298+06
96	squads	0002_auto_20181125_1624	2019-02-14 15:33:25.967669+06
97	squads	0003_squadweek	2019-02-14 15:33:26.08971+06
98	squads	0004_squadweek_dates	2019-02-14 15:33:26.279223+06
99	squads	0005_remove_squadweek_dates	2019-02-14 15:33:26.312324+06
100	squads	0006_squadweek_actual	2019-02-14 15:33:26.434925+06
101	squads	0007_squad_cabinet	2019-02-14 15:33:26.613292+06
102	squads	0008_auto_20181128_0424	2019-02-14 15:33:26.746306+06
103	squads	0009_auto_20181130_0614	2019-02-14 15:33:26.801801+06
104	squads	0010_remove_squad_cabinet	2019-02-14 15:33:26.835315+06
105	squads	0011_squadweek_active	2019-02-14 15:33:26.946578+06
106	squads	0012_remove_squadweek_active	2019-02-14 15:33:26.979668+06
107	squads	0013_auto_20181211_0250	2019-02-14 15:33:27.113465+06
108	squads	0014_auto_20181211_0623	2019-02-14 15:33:27.157406+06
109	squads	0015_squad_cabinet	2019-02-14 15:33:27.347381+06
110	subjects	0001_initial	2019-02-14 15:33:28.651147+06
111	subjects	0002_auto_20181122_0834	2019-02-14 15:33:28.895573+06
112	subjects	0003_auto_20181122_0843	2019-02-14 15:33:28.962308+06
113	subjects	0004_subject_lesson_ids	2019-02-14 15:33:29.162936+06
114	subjects	0005_auto_20181125_0323	2019-02-14 15:33:29.574705+06
115	subjects	0006_squadorder	2019-02-14 15:33:29.875301+06
116	subjects	0007_auto_20181125_0511	2019-02-14 15:33:30.008527+06
117	subjects	0008_day_number	2019-02-14 15:33:30.108912+06
118	subjects	0009_auto_20181125_0652	2019-02-14 15:33:30.183237+06
119	subjects	0010_auto_20181125_0658	2019-02-14 15:33:30.220087+06
120	subjects	0011_auto_20181125_0659	2019-02-14 15:33:30.27288+06
121	subjects	0012_auto_20181125_1849	2019-02-14 15:33:30.555738+06
122	subjects	0013_auto_20181126_1402	2019-02-14 15:33:30.622405+06
123	subjects	0014_auto_20181126_1403	2019-02-14 15:33:31.37959+06
124	subjects	0015_auto_20181126_2227	2019-02-14 15:33:31.891245+06
125	subjects	0016_remove_lecture_time_period	2019-02-14 15:33:31.96869+06
126	subjects	0017_auto_20181127_0114	2019-02-14 15:33:32.313859+06
127	subjects	0018_squadcell_time_period	2019-02-14 15:33:32.42481+06
128	subjects	0019_auto_20181127_0210	2019-02-14 15:33:32.780989+06
129	subjects	0020_auto_20181127_1630	2019-02-14 15:33:32.819159+06
130	subjects	0021_attendance	2019-02-14 15:33:33.025719+06
131	subjects	0022_auto_20181128_0447	2019-02-14 15:33:33.30354+06
132	subjects	0023_auto_20181128_0501	2019-02-14 15:33:33.350269+06
133	subjects	0024_auto_20181128_0514	2019-02-14 15:33:33.392683+06
134	subjects	0025_subject_number_of_lectures	2019-02-14 15:33:33.604329+06
135	subjects	0026_auto_20181130_0614	2019-02-14 15:33:33.693067+06
136	subjects	0027_subject_cabinet	2019-02-14 15:33:33.904698+06
137	subjects	0028_auto_20181209_0521	2019-02-14 15:33:34.350272+06
138	subjects	0029_auto_20181209_0659	2019-02-14 15:33:34.850956+06
139	subjects	0030_auto_20181209_0809	2019-02-14 15:33:34.939289+06
140	subjects	0031_auto_20181209_1606	2019-02-14 15:33:35.239316+06
141	subjects	0032_auto_20181209_1655	2019-02-14 15:33:35.417483+06
142	subjects	0033_auto_20181209_1658	2019-02-14 15:33:35.818364+06
143	subjects	0034_auto_20181209_1715	2019-02-14 15:33:35.962671+06
144	subjects	0035_subject_students	2019-02-14 15:33:36.196225+06
145	subjects	0036_auto_20181226_1750	2019-02-14 15:33:36.341047+06
146	subjects	0037_auto_20181226_1812	2019-02-14 15:33:36.388732+06
147	subjects	0038_attendance_subject_materials	2019-02-14 15:33:36.496411+06
148	subjects	0039_auto_20181230_1530	2019-02-14 15:33:37.321027+06
149	subjects	0040_subject_color_back	2019-02-14 15:33:37.509981+06
150	subjects	0041_auto_20190121_1435	2019-02-14 15:33:38.032972+06
151	subjects	0042_subjectmaterials_done_by	2019-02-14 15:33:38.288119+06
152	tasks	0002_auto_20181202_1704	2019-02-14 15:33:38.411014+06
153	tasks	0003_auto_20181202_1710	2019-02-14 15:33:38.477643+06
154	tasks	0004_auto_20181202_1710	2019-02-14 15:33:38.544335+06
155	tasks	0005_auto_20181217_2150	2019-02-14 15:33:39.003114+06
156	tasks	0006_auto_20190117_1100	2019-02-14 15:33:39.050369+06
157	tasks	0007_auto_20190118_2153	2019-02-14 15:33:39.147448+06
158	tasks	0008_auto_20190125_1953	2019-02-14 15:33:39.271365+06
168	accounts	0038_auto_20190216_1648	2019-02-16 16:48:15.235832+06
169	subjects	0043_auto_20190216_1648	2019-02-16 16:48:15.426187+06
170	accounts	0039_auto_20190216_1731	2019-02-16 17:31:35.564917+06
171	documents	0003_documentfolder_school	2019-02-17 13:36:11.259666+06
172	library	0005_auto_20190217_1336	2019-02-17 13:36:11.832236+06
173	news	0004_post_school	2019-02-17 13:36:12.12076+06
174	papers	0026_auto_20190217_1336	2019-02-17 13:36:12.900699+06
175	squads	0016_squad_school	2019-02-17 13:36:13.168157+06
176	subjects	0044_auto_20190217_1336	2019-02-17 13:36:15.221091+06
177	tasks	0009_auto_20190217_1336	2019-02-17 13:36:15.343977+06
178	todolist	0002_auto_20190217_1336	2019-02-17 13:36:15.688297+06
179	schools	0003_auto_20190217_1514	2019-02-17 15:14:15.637923+06
180	accounts	0040_auto_20190217_1514	2019-02-17 15:14:15.93969+06
181	subjects	0045_timeperiod_students	2019-02-17 15:28:06.839908+06
182	papers	0027_lesson_access_to_everyone	2019-02-19 04:12:20.3642+06
183	accounts	0041_zaiavka_school	2019-02-19 04:36:29.27058+06
184	accounts	0042_auto_20190220_2014	2019-02-20 20:14:44.426995+06
185	accounts	0043_auto_20190220_2026	2019-02-20 20:26:32.785825+06
186	accounts	0044_profile_salary	2019-02-20 20:43:01.120102+06
187	schools	0004_cabinet	2019-02-22 18:55:52.888009+06
188	subjects	0046_auto_20190222_1855	2019-02-22 18:55:54.016571+06
189	squads	0017_auto_20190222_1855	2019-02-22 18:55:54.373639+06
190	squads	0018_delete_squadweek	2019-02-22 18:55:54.394993+06
191	accounts	0045_auto_20190223_2219	2019-02-23 22:19:51.858271+06
192	accounts	0046_profile_job_categories	2019-02-23 22:28:35.130828+06
193	subjects	0047_auto_20190224_2136	2019-02-24 21:36:30.521255+06
194	subjects	0048_auto_20190224_2154	2019-02-24 21:54:21.953943+06
195	subjects	0049_auto_20190226_0638	2019-02-26 06:39:03.803947+06
196	accounts	0047_auto_20190226_0642	2019-02-26 06:43:00.390451+06
197	schools	0005_auto_20190227_0559	2019-02-27 05:59:41.644631+06
198	schools	0005_auto_20190227_0603	2019-02-27 06:04:07.772287+06
199	subjects	0050_auto_20190227_0603	2019-02-27 06:04:07.789452+06
200	schools	0006_auto_20190227_0611	2019-02-27 06:11:14.74561+06
201	subjects	0050_auto_20190227_0616	2019-02-27 06:16:14.967305+06
202	subjects	0051_auto_20190227_0620	2019-02-27 06:20:42.678703+06
203	subjects	0052_auto_20190227_0621	2019-02-27 06:21:38.648982+06
204	subjects	0051_auto_20190227_0626	2019-02-27 06:26:08.805641+06
205	papers	0028_auto_20190227_0647	2019-02-27 06:47:35.609674+06
206	schools	0007_auto_20190227_0647	2019-02-27 06:47:35.96987+06
207	tasks	0010_auto_20190227_0647	2019-02-27 06:47:36.035627+06
208	subjects	0051_auto_20190227_0648	2019-02-27 06:49:03.951874+06
209	accounts	0048_auto_20190228_0907	2019-02-28 09:07:16.189706+06
210	subjects	0052_auto_20190228_1132	2019-02-28 11:32:05.418203+06
211	schools	0008_auto_20190301_0303	2019-03-01 03:03:56.566597+06
212	subjects	0053_auto_20190301_0303	2019-03-01 03:03:56.979982+06
213	subjects	0054_subject_cost	2019-03-02 05:32:05.117271+06
214	subjects	0055_lecture_color_back	2019-03-02 07:10:53.843899+06
215	squads	0019_auto_20190302_0716	2019-03-02 07:16:32.287697+06
216	subjects	0056_remove_lecture_color_back	2019-03-02 07:16:32.376265+06
217	accounts	0049_misslesson	2019-03-07 16:35:41.499454+06
218	accounts	0050_auto_20190307_1706	2019-03-07 17:06:33.481006+06
219	accounts	0051_auto_20190307_1739	2019-03-07 17:40:04.816476+06
220	accounts	0052_auto_20190307_1744	2019-03-07 17:44:43.27118+06
221	accounts	0053_auto_20190309_1057	2019-03-09 10:57:09.000054+06
222	subjects	0057_cacheattendance	2019-03-09 10:57:09.604094+06
223	subjects	0058_auto_20190309_1058	2019-03-09 10:58:18.585841+06
224	subjects	0059_lecture_day	2019-03-09 13:34:45.730783+06
225	accounts	0054_profile_is_student	2019-03-12 18:53:57.316716+06
226	accounts	0055_auto_20190312_1854	2019-03-12 18:54:25.205962+06
227	subjects	0060_auto_20190315_0423	2019-03-15 04:23:25.399077+06
228	subjects	0061_auto_20190315_2138	2019-03-15 21:38:20.977574+06
229	subjects	0062_auto_20190316_1614	2019-03-16 16:14:03.90844+06
230	subjects	0063_auto_20190320_0353	2019-03-20 03:54:06.930437+06
231	schools	0009_auto_20190407_1713	2019-04-07 17:13:31.569565+06
232	accounts	0056_auto_20190407_1713	2019-04-07 17:13:32.420227+06
233	accounts	0057_auto_20190407_2047	2019-04-07 20:47:22.758619+06
234	subjects	0064_auto_20190410_0341	2019-04-10 03:41:23.316955+06
235	accounts	0058_crmcard_saved	2019-04-10 05:44:04.056658+06
236	accounts	0059_profile_hint	2019-04-10 08:23:47.465484+06
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
ge527a10caw1i79npreergz8c3edsz5z	ZWU5ZWI4OWVhNDFjYTdhMWJiMWI0NTZiYjI5MmRjZmUwMzIyMzZhNjp7Il9hdXRoX3VzZXJfaWQiOiIxMDgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjQ3YmFlMmE2NjFmNzMzYTVjMDlhZDM4MGJkMjQxY2E0Y2JhZTIzZjUifQ==	2019-04-24 11:00:01.664249+06
nzkkqockzkkcuo4400xgnslh430xojqr	ZjlhNTllOTlhOGQ3ZjEyOGIwMDQwMThlNzZkMDE1MzQwNzdkMWNiMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzZhYzM0YWIyMDQyMzJlMTc2N2E3MmI2N2Y2ZjA4MzYxNjM1NzE5In0=	2018-12-30 05:47:35.971604+06
3hj4aynjb5s2k5srkk3f9l8pau8ydyxa	ZTczZTMxZjllMmQ4ZDAzNTU4MjFiMTExMDQxMzgxY2MzYWVhNTBkMTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxOGI5YzVmN2Q1YmJiMjMzN2QwZDE3ZTc3ZWViZmUxNzhkNzNjMTZmIn0=	2018-12-09 04:51:52.972922+06
msp2s7ixlrvcdo5s3ok78pbtigreklkz	ZTg3NTEwMTc2MmIxNDhiZDUyODNjZWNjNjBiYmQ4Mjk1ZTYyYjE2ZTp7Il9hdXRoX3VzZXJfaWQiOiIzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjYWRkMmI3MzEyZmQyMDgwODM2MjBjZTlkMWQ0OTk5NjI1MDZmZDhmIn0=	2018-12-16 14:58:54.300532+06
llescqvtp1a966evxh7scl8spxgyr3kf	NmRjODNlZjRmN2Y5YTI2NjFhM2YwZTI5ZDk4NTczMGQzYmRkYmJlNTp7fQ==	2018-12-16 18:16:52.063159+06
y185qc5dez6wq667an8mf6mbsu8jtcyl	NmRjODNlZjRmN2Y5YTI2NjFhM2YwZTI5ZDk4NTczMGQzYmRkYmJlNTp7fQ==	2018-12-16 18:35:47.625583+06
c926l1yvl7yt7cluhbyn4v4one5y22tv	NmRjODNlZjRmN2Y5YTI2NjFhM2YwZTI5ZDk4NTczMGQzYmRkYmJlNTp7fQ==	2018-12-16 18:35:49.898442+06
h8x5h4k161ajqtwqmsokdgrv9p2t47ot	NmRjODNlZjRmN2Y5YTI2NjFhM2YwZTI5ZDk4NTczMGQzYmRkYmJlNTp7fQ==	2018-12-16 18:36:34.658338+06
8f501gxd3sbqko24zq9nkiiy2wzzp7uq	NmRjODNlZjRmN2Y5YTI2NjFhM2YwZTI5ZDk4NTczMGQzYmRkYmJlNTp7fQ==	2018-12-16 19:09:51.605253+06
xa79rksmr6au97tpyghuevn53678mtbr	NmRjODNlZjRmN2Y5YTI2NjFhM2YwZTI5ZDk4NTczMGQzYmRkYmJlNTp7fQ==	2018-12-16 19:19:47.948632+06
2vzg31kgyqriu6rn4eb085gbpotsbvir	NmRjODNlZjRmN2Y5YTI2NjFhM2YwZTI5ZDk4NTczMGQzYmRkYmJlNTp7fQ==	2018-12-16 19:19:55.447157+06
aehzolp11i5k4t7qqzm98k9jdk368z0l	ZTg3NTEwMTc2MmIxNDhiZDUyODNjZWNjNjBiYmQ4Mjk1ZTYyYjE2ZTp7Il9hdXRoX3VzZXJfaWQiOiIzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjYWRkMmI3MzEyZmQyMDgwODM2MjBjZTlkMWQ0OTk5NjI1MDZmZDhmIn0=	2018-12-16 19:23:43.464584+06
ga83qpizs1z4eo3v3y5lagbbfd8yi8l4	Njc1ZDBiMTZkMDVhNjJmNWY0MWQ5OWQ3YjM5YWVlYzFkOTRlYmYwNzp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwMWRlNzdjMTBhYTM3YmZjOGI5NjRkMzg5ODExMGI5YTU5MzNiMGZlIn0=	2018-12-21 18:44:39.202161+06
87p03iz4qt9g9dwkht5l1wh8ah2incv9	NmRjODNlZjRmN2Y5YTI2NjFhM2YwZTI5ZDk4NTczMGQzYmRkYmJlNTp7fQ==	2018-12-29 22:05:10.206596+06
ougzv799ocan51cvj8uic7yzma4xomny	NmRjODNlZjRmN2Y5YTI2NjFhM2YwZTI5ZDk4NTczMGQzYmRkYmJlNTp7fQ==	2018-12-30 04:05:02.221397+06
9yscexjudn639jk9tmwk8j8049u4lc5r	NmRjODNlZjRmN2Y5YTI2NjFhM2YwZTI5ZDk4NTczMGQzYmRkYmJlNTp7fQ==	2018-12-30 04:05:18.40117+06
zsdiw8kf4clpes0xhu86ikjg11f2319q	NmRjODNlZjRmN2Y5YTI2NjFhM2YwZTI5ZDk4NTczMGQzYmRkYmJlNTp7fQ==	2018-12-30 04:05:27.6326+06
u4s1h3a06m3q43kqnubmj02c6biconun	NmRjODNlZjRmN2Y5YTI2NjFhM2YwZTI5ZDk4NTczMGQzYmRkYmJlNTp7fQ==	2018-12-30 04:08:44.089015+06
lqdg0prwnxlrpyon0wsejhcobeuq1xai	NmRjODNlZjRmN2Y5YTI2NjFhM2YwZTI5ZDk4NTczMGQzYmRkYmJlNTp7fQ==	2018-12-30 04:08:54.853978+06
n1qu8v15agx5tjc7i7wu7g6nxrj8bpdm	NmRjODNlZjRmN2Y5YTI2NjFhM2YwZTI5ZDk4NTczMGQzYmRkYmJlNTp7fQ==	2018-12-30 04:09:40.500722+06
lsdtmrisuygh2efq1htxmmumfeu2o16a	Y2YwZmVjMjc2YmM4MmIwZTkwNWJiYzFlYmQxNDFhNTUyZjBhZjVkNjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhMTliNmRhZWU5ZmJlN2ZiMzU3ZDM1NzljMDZhMmYyMWFiNmFmNGVkIn0=	2018-12-30 04:11:43.044588+06
kk355hzedfehnea6dk84sghvb3xx691m	Nzk2NmM5ZDdlNTBmMzJhMTEwMGQyYWYwYjJjZjQ4ODRmZTI4YzdkMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlMDAzZmU0YWFhZTkxNzZmOWRkNDJkZGRkN2IwM2M1ZmUzN2E2NWMyIn0=	2018-12-30 04:14:09.327194+06
jgsuvrzhz5egs51qyaxcudou7b7y9exr	NmRjODNlZjRmN2Y5YTI2NjFhM2YwZTI5ZDk4NTczMGQzYmRkYmJlNTp7fQ==	2018-12-30 04:59:03.292012+06
b07v9zupmefrt8h35t8ri68lm7g3q9ds	Zjk5Y2EyZTk2ZDJjMzJiNDYzOTg2ZmJhMDE2NDZjY2YzZmJhZDE3MDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxNTI1MDQ3NDNjMWNmMDk2NTcwNTc3OGJjZmNlOGZhNmU5NDE3ZDMzIn0=	2018-12-30 05:09:11.585948+06
xnrsr2iw8ye4omuqtja4mqw4mowagztv	NTE0YWU0MzA4MjViOTk4NzBiYmJhZGQ3NzhkNjFiNDZlZDBjMWI2Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxOGQ4YzQ1YTk4N2Q1YThjMjkzMTZlZTFkM2ZkZDJjNTdlMjdkMmI3In0=	2018-12-30 05:12:17.231203+06
pl4n3qi1ktk55fkb44zrfjthakxowswe	NTE0YWU0MzA4MjViOTk4NzBiYmJhZGQ3NzhkNjFiNDZlZDBjMWI2Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxOGQ4YzQ1YTk4N2Q1YThjMjkzMTZlZTFkM2ZkZDJjNTdlMjdkMmI3In0=	2018-12-30 05:15:38.33138+06
333nwldoj7fmdn43sst3q61enxt2kq98	NmRjODNlZjRmN2Y5YTI2NjFhM2YwZTI5ZDk4NTczMGQzYmRkYmJlNTp7fQ==	2018-12-30 05:19:40.566949+06
mwq8l8wytypauhstlhifhoruakzafy9a	NTE0YWU0MzA4MjViOTk4NzBiYmJhZGQ3NzhkNjFiNDZlZDBjMWI2Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxOGQ4YzQ1YTk4N2Q1YThjMjkzMTZlZTFkM2ZkZDJjNTdlMjdkMmI3In0=	2018-12-30 05:20:21.589404+06
ii7riofautynot12pmojbb7nhxzfeib7	NTE0YWU0MzA4MjViOTk4NzBiYmJhZGQ3NzhkNjFiNDZlZDBjMWI2Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxOGQ4YzQ1YTk4N2Q1YThjMjkzMTZlZTFkM2ZkZDJjNTdlMjdkMmI3In0=	2018-12-30 05:24:07.231412+06
cdutyh5g3wjis07detkhf3d9q359v2co	NTE0YWU0MzA4MjViOTk4NzBiYmJhZGQ3NzhkNjFiNDZlZDBjMWI2Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxOGQ4YzQ1YTk4N2Q1YThjMjkzMTZlZTFkM2ZkZDJjNTdlMjdkMmI3In0=	2018-12-30 05:25:59.640208+06
t04sexvvllsa6jgo1x4say94wpwt2sew	NTE0YWU0MzA4MjViOTk4NzBiYmJhZGQ3NzhkNjFiNDZlZDBjMWI2Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxOGQ4YzQ1YTk4N2Q1YThjMjkzMTZlZTFkM2ZkZDJjNTdlMjdkMmI3In0=	2018-12-30 05:27:45.230269+06
dypdi6fzcnxo0gw0ohk7am5um940e38k	NTE0YWU0MzA4MjViOTk4NzBiYmJhZGQ3NzhkNjFiNDZlZDBjMWI2Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxOGQ4YzQ1YTk4N2Q1YThjMjkzMTZlZTFkM2ZkZDJjNTdlMjdkMmI3In0=	2018-12-30 05:28:44.933645+06
p7a1i6f52ylfm85riuf09tu5mzxyu3fl	NTE0YWU0MzA4MjViOTk4NzBiYmJhZGQ3NzhkNjFiNDZlZDBjMWI2Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxOGQ4YzQ1YTk4N2Q1YThjMjkzMTZlZTFkM2ZkZDJjNTdlMjdkMmI3In0=	2018-12-30 05:32:33.324796+06
st1dbvstivbtndf4r952k7jyqu45n4vb	NTE0YWU0MzA4MjViOTk4NzBiYmJhZGQ3NzhkNjFiNDZlZDBjMWI2Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxOGQ4YzQ1YTk4N2Q1YThjMjkzMTZlZTFkM2ZkZDJjNTdlMjdkMmI3In0=	2018-12-30 05:34:54.463329+06
zc1qb33xoqeu0td4a9c2zaur39phi7tu	NTE0YWU0MzA4MjViOTk4NzBiYmJhZGQ3NzhkNjFiNDZlZDBjMWI2Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxOGQ4YzQ1YTk4N2Q1YThjMjkzMTZlZTFkM2ZkZDJjNTdlMjdkMmI3In0=	2018-12-30 05:36:58.944748+06
mesa6b0vlftpr61qpqr0i8bczvk1ydfs	ZjlhNTllOTlhOGQ3ZjEyOGIwMDQwMThlNzZkMDE1MzQwNzdkMWNiMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzZhYzM0YWIyMDQyMzJlMTc2N2E3MmI2N2Y2ZjA4MzYxNjM1NzE5In0=	2018-12-30 05:48:05.509706+06
w5rk84voxtg5u3jlpaxl61re9bzt0e4u	ZjlhNTllOTlhOGQ3ZjEyOGIwMDQwMThlNzZkMDE1MzQwNzdkMWNiMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzZhYzM0YWIyMDQyMzJlMTc2N2E3MmI2N2Y2ZjA4MzYxNjM1NzE5In0=	2018-12-30 05:48:59.96682+06
yj2ox861is7busvsdvb5b3akqgq1i0f5	ZjlhNTllOTlhOGQ3ZjEyOGIwMDQwMThlNzZkMDE1MzQwNzdkMWNiMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzZhYzM0YWIyMDQyMzJlMTc2N2E3MmI2N2Y2ZjA4MzYxNjM1NzE5In0=	2018-12-30 05:38:22.004182+06
p1to68g6mfbsie55wufy4u3qs8vn5dp1	ZjlhNTllOTlhOGQ3ZjEyOGIwMDQwMThlNzZkMDE1MzQwNzdkMWNiMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzZhYzM0YWIyMDQyMzJlMTc2N2E3MmI2N2Y2ZjA4MzYxNjM1NzE5In0=	2018-12-30 05:38:45.08369+06
q790bohvvyhenggr8zym5kez98ajd226	ZjlhNTllOTlhOGQ3ZjEyOGIwMDQwMThlNzZkMDE1MzQwNzdkMWNiMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzZhYzM0YWIyMDQyMzJlMTc2N2E3MmI2N2Y2ZjA4MzYxNjM1NzE5In0=	2018-12-30 05:39:33.821716+06
yxdm3py5gd58v3vp31n4qkhlhkpg18r1	NmRjODNlZjRmN2Y5YTI2NjFhM2YwZTI5ZDk4NTczMGQzYmRkYmJlNTp7fQ==	2018-12-30 05:45:07.357877+06
7ukv0wu7gae7u8vitkx58fyh1eaptqtf	ZjlhNTllOTlhOGQ3ZjEyOGIwMDQwMThlNzZkMDE1MzQwNzdkMWNiMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzZhYzM0YWIyMDQyMzJlMTc2N2E3MmI2N2Y2ZjA4MzYxNjM1NzE5In0=	2018-12-30 05:45:57.938856+06
m4tovscn53j74135cgn0g2sgpwobxd6f	ZjlhNTllOTlhOGQ3ZjEyOGIwMDQwMThlNzZkMDE1MzQwNzdkMWNiMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzZhYzM0YWIyMDQyMzJlMTc2N2E3MmI2N2Y2ZjA4MzYxNjM1NzE5In0=	2018-12-30 06:02:57.510997+06
28q9p3fi287w24we70lvy58h8s17pq5w	ZjlhNTllOTlhOGQ3ZjEyOGIwMDQwMThlNzZkMDE1MzQwNzdkMWNiMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzZhYzM0YWIyMDQyMzJlMTc2N2E3MmI2N2Y2ZjA4MzYxNjM1NzE5In0=	2018-12-30 05:46:20.714182+06
vnfzotawlx3sdkgt3lxhllidobnikmz1	ZjlhNTllOTlhOGQ3ZjEyOGIwMDQwMThlNzZkMDE1MzQwNzdkMWNiMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzZhYzM0YWIyMDQyMzJlMTc2N2E3MmI2N2Y2ZjA4MzYxNjM1NzE5In0=	2018-12-30 06:07:18.798165+06
tv5m9qxbluuq0vqteogyt2j6n4myi9ym	ZjlhNTllOTlhOGQ3ZjEyOGIwMDQwMThlNzZkMDE1MzQwNzdkMWNiMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzZhYzM0YWIyMDQyMzJlMTc2N2E3MmI2N2Y2ZjA4MzYxNjM1NzE5In0=	2018-12-30 06:08:02.335726+06
00p02yptzyd4jt4sxhlpogoxeh84ws9o	ZjlhNTllOTlhOGQ3ZjEyOGIwMDQwMThlNzZkMDE1MzQwNzdkMWNiMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzZhYzM0YWIyMDQyMzJlMTc2N2E3MmI2N2Y2ZjA4MzYxNjM1NzE5In0=	2018-12-30 18:04:19.19212+06
6zefje20q5rmw5oaa9c0679yqed6k2t8	NmRjODNlZjRmN2Y5YTI2NjFhM2YwZTI5ZDk4NTczMGQzYmRkYmJlNTp7fQ==	2018-12-30 19:31:37.146745+06
5l6zfbh0qsx9pdoe2gcpanigxj74zggj	ZjlhNTllOTlhOGQ3ZjEyOGIwMDQwMThlNzZkMDE1MzQwNzdkMWNiMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzZhYzM0YWIyMDQyMzJlMTc2N2E3MmI2N2Y2ZjA4MzYxNjM1NzE5In0=	2018-12-30 19:31:49.269128+06
oom2d7w47zcb4mjm9oitbclef26bi344	Njg0ZjkwYWQ5OTExZDUwNzBmZTQ2OGU3NTdjNGRiNGU2MjFjYWEzMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1YjRiYzJlMjM2NzM4MzZmNDJiOWY2OWVmODI4MGE2YTdiYWNiMjE2In0=	2018-12-31 20:16:47.331164+06
lcy5r6h28fyagy7tnzr5whvjat2tfnhg	ZjlhNTllOTlhOGQ3ZjEyOGIwMDQwMThlNzZkMDE1MzQwNzdkMWNiMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzZhYzM0YWIyMDQyMzJlMTc2N2E3MmI2N2Y2ZjA4MzYxNjM1NzE5In0=	2019-01-04 09:42:21.753146+06
qoqubftg2045vrfivttv9lycu3q5x0r6	NmRjODNlZjRmN2Y5YTI2NjFhM2YwZTI5ZDk4NTczMGQzYmRkYmJlNTp7fQ==	2019-01-07 10:16:21.850088+06
0d5xmv9deynw1zy70afrv0so2sh54k3s	NmRjODNlZjRmN2Y5YTI2NjFhM2YwZTI5ZDk4NTczMGQzYmRkYmJlNTp7fQ==	2019-01-07 10:16:29.364969+06
i1ay662polqx3qjvrabl7ahyl795rxmu	NmRjODNlZjRmN2Y5YTI2NjFhM2YwZTI5ZDk4NTczMGQzYmRkYmJlNTp7fQ==	2019-01-07 10:16:47.20269+06
pkdqk6hwotxnd8cdmgdxoz07gbbyr45q	NDA0NDUyNjFjZTllNDU4YTQ0MzdhY2M0NTNiNWMyYTVlZWI2YzllMDp7Il9hdXRoX3VzZXJfaWQiOiIxMiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYzViMDFlZWI0ZDU1OTMyMzdmYzU3YmJkZWJkZjRkMTM2OTY0OWYzYyJ9	2019-01-07 10:20:18.430792+06
ecvzqlakmjp1gfs3rxf81ui6k7bpdpwo	Njg0ZjkwYWQ5OTExZDUwNzBmZTQ2OGU3NTdjNGRiNGU2MjFjYWEzMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1YjRiYzJlMjM2NzM4MzZmNDJiOWY2OWVmODI4MGE2YTdiYWNiMjE2In0=	2019-01-08 06:57:35.837445+06
oh517z7e6gcmaxeb7ounb2q5vcvqkma1	Njg0ZjkwYWQ5OTExZDUwNzBmZTQ2OGU3NTdjNGRiNGU2MjFjYWEzMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1YjRiYzJlMjM2NzM4MzZmNDJiOWY2OWVmODI4MGE2YTdiYWNiMjE2In0=	2019-01-08 14:11:57.339396+06
142r7sr4dlo1s1q9qwrkx11i2i98d5ep	Njg0ZjkwYWQ5OTExZDUwNzBmZTQ2OGU3NTdjNGRiNGU2MjFjYWEzMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1YjRiYzJlMjM2NzM4MzZmNDJiOWY2OWVmODI4MGE2YTdiYWNiMjE2In0=	2019-01-09 12:13:40.85727+06
6amu39imbf946khuvwd6s8x04cgssp8o	Njg0ZjkwYWQ5OTExZDUwNzBmZTQ2OGU3NTdjNGRiNGU2MjFjYWEzMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1YjRiYzJlMjM2NzM4MzZmNDJiOWY2OWVmODI4MGE2YTdiYWNiMjE2In0=	2019-01-12 21:17:43.491905+06
gyw061br2ndpkilzztwghmqo2dbzaoec	Njg0ZjkwYWQ5OTExZDUwNzBmZTQ2OGU3NTdjNGRiNGU2MjFjYWEzMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1YjRiYzJlMjM2NzM4MzZmNDJiOWY2OWVmODI4MGE2YTdiYWNiMjE2In0=	2019-01-15 13:10:05.007902+06
r4tey1wgyq4ggg2dy39skct5f0g5j365	Njg0ZjkwYWQ5OTExZDUwNzBmZTQ2OGU3NTdjNGRiNGU2MjFjYWEzMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1YjRiYzJlMjM2NzM4MzZmNDJiOWY2OWVmODI4MGE2YTdiYWNiMjE2In0=	2019-01-16 14:33:47.41984+06
9q37gl2n3462v04npegci75jtl0rf0ud	ZjlhNTllOTlhOGQ3ZjEyOGIwMDQwMThlNzZkMDE1MzQwNzdkMWNiMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzZhYzM0YWIyMDQyMzJlMTc2N2E3MmI2N2Y2ZjA4MzYxNjM1NzE5In0=	2019-01-19 19:09:18.596968+06
adv5ra3573ko87cycmbub25rd2f4mend	Njg0ZjkwYWQ5OTExZDUwNzBmZTQ2OGU3NTdjNGRiNGU2MjFjYWEzMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1YjRiYzJlMjM2NzM4MzZmNDJiOWY2OWVmODI4MGE2YTdiYWNiMjE2In0=	2019-01-21 22:34:15.258516+06
a5zyshsteagtnwtvfoa0nnv1oc5cjl3i	Njg0ZjkwYWQ5OTExZDUwNzBmZTQ2OGU3NTdjNGRiNGU2MjFjYWEzMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1YjRiYzJlMjM2NzM4MzZmNDJiOWY2OWVmODI4MGE2YTdiYWNiMjE2In0=	2019-01-22 16:49:29.805065+06
s86gq5nkafaeslhvvopwrje32kwkq6ej	Njg0ZjkwYWQ5OTExZDUwNzBmZTQ2OGU3NTdjNGRiNGU2MjFjYWEzMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1YjRiYzJlMjM2NzM4MzZmNDJiOWY2OWVmODI4MGE2YTdiYWNiMjE2In0=	2019-01-23 16:05:43.866947+06
ci0xome1slokhsb3mgfavs4ujp9m4qc2	Njg0ZjkwYWQ5OTExZDUwNzBmZTQ2OGU3NTdjNGRiNGU2MjFjYWEzMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1YjRiYzJlMjM2NzM4MzZmNDJiOWY2OWVmODI4MGE2YTdiYWNiMjE2In0=	2019-01-23 20:15:35.996923+06
krpta6k9vvxprewk6i5rsmp7m6u4jd6a	Njg0ZjkwYWQ5OTExZDUwNzBmZTQ2OGU3NTdjNGRiNGU2MjFjYWEzMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1YjRiYzJlMjM2NzM4MzZmNDJiOWY2OWVmODI4MGE2YTdiYWNiMjE2In0=	2019-01-31 11:04:28.124665+06
hjq1jxq2m7ccfaljylnepmfycj6lmvyy	Njg0ZjkwYWQ5OTExZDUwNzBmZTQ2OGU3NTdjNGRiNGU2MjFjYWEzMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1YjRiYzJlMjM2NzM4MzZmNDJiOWY2OWVmODI4MGE2YTdiYWNiMjE2In0=	2019-02-01 09:34:31.41644+06
05ekyk80fc8kd4utfpz054x7ncna226d	ZjlhNTllOTlhOGQ3ZjEyOGIwMDQwMThlNzZkMDE1MzQwNzdkMWNiMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzZhYzM0YWIyMDQyMzJlMTc2N2E3MmI2N2Y2ZjA4MzYxNjM1NzE5In0=	2019-02-02 22:30:16.885798+06
l6witz6123bnd07ym8stqmav3urn2o0n	Njg0ZjkwYWQ5OTExZDUwNzBmZTQ2OGU3NTdjNGRiNGU2MjFjYWEzMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1YjRiYzJlMjM2NzM4MzZmNDJiOWY2OWVmODI4MGE2YTdiYWNiMjE2In0=	2019-02-04 23:46:49.720584+06
92xeetpieqkod4bpjydpv9rse5ffw5ie	Njg0ZjkwYWQ5OTExZDUwNzBmZTQ2OGU3NTdjNGRiNGU2MjFjYWEzMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1YjRiYzJlMjM2NzM4MzZmNDJiOWY2OWVmODI4MGE2YTdiYWNiMjE2In0=	2019-02-07 21:11:34.167639+06
1vrgjomfptyk1icvwv5c2xfd4ledy8xz	Njg0ZjkwYWQ5OTExZDUwNzBmZTQ2OGU3NTdjNGRiNGU2MjFjYWEzMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1YjRiYzJlMjM2NzM4MzZmNDJiOWY2OWVmODI4MGE2YTdiYWNiMjE2In0=	2019-02-10 08:53:13.370751+06
bn8bcd0kyzoa62uy61xu7ybbvl80i8os	Njg0ZjkwYWQ5OTExZDUwNzBmZTQ2OGU3NTdjNGRiNGU2MjFjYWEzMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1YjRiYzJlMjM2NzM4MzZmNDJiOWY2OWVmODI4MGE2YTdiYWNiMjE2In0=	2019-02-14 02:21:31.439245+06
nqui6veco2aas87bpyg77wdoe45yh5bq	MjA2MTQ4NTRhZTEzZjE2NjVkOGJhZjZlM2ExNjA5MzM4YTJmNTRjMjp7Il9hdXRoX3VzZXJfaWQiOiI5NCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZWJmNDI4MjFkYWZlODFhZmVjZGYzYTI3MjA4YTE1MTJkMDA4NjM4YyJ9	2019-02-25 21:05:24.234659+06
00qg979hazs07k7bucuvpvuhpmt40dzg	ZjlhNTllOTlhOGQ3ZjEyOGIwMDQwMThlNzZkMDE1MzQwNzdkMWNiMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzZhYzM0YWIyMDQyMzJlMTc2N2E3MmI2N2Y2ZjA4MzYxNjM1NzE5In0=	2019-02-26 14:19:25.947087+06
7zpmsjvr0m7n8uy5p9b2vtapdj5w9o60	ZGVmZjk3ZjZjMzNlODUyMGZhNjcyMWY4ZThhODg5OGViZjYwNzQwNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5Y2U4ZmQ0MTc4ZWViZjFiOGQ4ZTY1OTI1MTUwMDNjNWU4OWU5NWJkIn0=	2019-04-28 17:55:13.328543+06
r2g5zty4mstf4q341xs2hwse7cb5jpxt	NzYwYzcwMTlhY2ZmMmIyZGE2NTJmYTU1Y2ZiOTNiMTExZmY0N2E2Yjp7Il9hdXRoX3VzZXJfaWQiOiI5NSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOGVkNGRhYmUxNTc5NDQwOTJjMjk2ZTFhYjAwNzUyNmYzOTEyYjNjYyJ9	2019-03-03 11:03:29.904725+06
cs56rq6tgpzng1zb5bk7x4zefnm7he1a	ZGVmZjk3ZjZjMzNlODUyMGZhNjcyMWY4ZThhODg5OGViZjYwNzQwNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5Y2U4ZmQ0MTc4ZWViZjFiOGQ4ZTY1OTI1MTUwMDNjNWU4OWU5NWJkIn0=	2019-03-05 12:17:32.380697+06
q7ka5xbmcm9vqpuove0m1jazmze6bohp	NzYwYzcwMTlhY2ZmMmIyZGE2NTJmYTU1Y2ZiOTNiMTExZmY0N2E2Yjp7Il9hdXRoX3VzZXJfaWQiOiI5NSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOGVkNGRhYmUxNTc5NDQwOTJjMjk2ZTFhYjAwNzUyNmYzOTEyYjNjYyJ9	2019-03-10 18:03:58.158151+06
agez7e3h2r45t98ruh8n1qqy0l2aif30	YjI4MDM3YTZkNTFkMjg4MTA0MWRmNTRmMGYzNjdhOTQ4MWJjOThmOTp7Il9hdXRoX3VzZXJfaWQiOiIxMDAiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImYzODZhMzkyNzRhMjY0NzBhMmQ2NTU2YjFjMTk1OWI5MDdjY2RjMDkifQ==	2019-03-16 07:46:42.416927+06
9tcp6by1lvz93xvpnvhf45romwt9n908	ZGVmZjk3ZjZjMzNlODUyMGZhNjcyMWY4ZThhODg5OGViZjYwNzQwNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5Y2U4ZmQ0MTc4ZWViZjFiOGQ4ZTY1OTI1MTUwMDNjNWU4OWU5NWJkIn0=	2019-03-19 19:51:37.046133+06
bbjvuk89z0yikcofeskae6ktsxfqju66	NzYwYzcwMTlhY2ZmMmIyZGE2NTJmYTU1Y2ZiOTNiMTExZmY0N2E2Yjp7Il9hdXRoX3VzZXJfaWQiOiI5NSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOGVkNGRhYmUxNTc5NDQwOTJjMjk2ZTFhYjAwNzUyNmYzOTEyYjNjYyJ9	2019-03-21 19:30:23.610028+06
6mcgqsk7d1nq1du1zerrls9bmgwyxv66	YTBiMTIwYWJiOTIzZDZhNmQ2YTFlNTk1ZGY1OGQzNTUzNGE2NTkyOTp7Il9hdXRoX3VzZXJfaWQiOiI5NSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOGVkNGRhYmUxNTc5NDQwOTJjMjk2ZTFhYjAwNzUyNmYzOTEyYjNjYyIsImhpbnQiOjB9	2019-04-15 17:17:34.095264+06
f8nxb4laldh13q7xnqw2ygskxgvm4uwm	YjkxNmVhZmY1YWYzZTlkZTRiNjY5ZWU0ZDBiMmFkM2JjNTcxZDEzOTp7Il9hdXRoX3VzZXJfaWQiOiIxMDUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImI5NWIyYzllZTkzZDRiOTJmMWFhZTI3MGQ5NjhlOWUxMTNlYzNmYTYiLCJoaW50IjowfQ==	2019-04-19 14:54:18.0702+06
vrt97etq7rg4s8q78kzs9uz6lihp7jwv	MWU5OTM2YzlmNjI2ZjY4YjZmNDc4MmEzOGUxMDAzNzYxZjJjZTkxNjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5Y2U4ZmQ0MTc4ZWViZjFiOGQ4ZTY1OTI1MTUwMDNjNWU4OWU5NWJkIiwiaGludCI6MTAwfQ==	2019-04-24 06:45:28.116732+06
q83pr5x6y0f6htu67xtlqe24kfvyvjhu	OGNhYTVhOTg3NGE1OTBhNWNjYzhiNzM2YmQ0YTk2ZTg0YzE0ZDFlNzp7Il9hdXRoX3VzZXJfaWQiOiIxMDgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjQ3YmFlMmE2NjFmNzMzYTVjMDlhZDM4MGJkMjQxY2E0Y2JhZTIzZjUiLCJoaW50IjowfQ==	2019-04-21 12:30:03.039906+06
\.


--
-- Data for Name: docs_board; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.docs_board (id, name) FROM stdin;
1	ff
3	kk
\.


--
-- Data for Name: docs_card; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.docs_card (id, title, slug, description, column_id) FROM stdin;
2	kmnk	kmnk		2
3	k	k		2
4	kkk	kkk		2
5	kk	kk	fjnjfrnfjrnf	1
\.


--
-- Data for Name: docs_card_doc_list; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.docs_card_doc_list (id, card_id, document_id) FROM stdin;
1	5	1
\.


--
-- Data for Name: docs_card_metka_list; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.docs_card_metka_list (id, card_id, metka_id) FROM stdin;
1	5	1
2	5	2
\.


--
-- Data for Name: docs_card_user_list; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.docs_card_user_list (id, card_id, profile_id) FROM stdin;
3	5	1
14	5	6
16	5	12
17	5	13
\.


--
-- Data for Name: docs_column; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.docs_column (id, title, board_id) FROM stdin;
1	ww	1
2	kmk	1
3	kkk4	1
\.


--
-- Data for Name: docs_comment; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.docs_comment (id, content, "timestamp", image, height_field, width_field, author_profile_id, card_id) FROM stdin;
1	mkmk	2019-01-13 21:13:20.889018+06		0	0	1	5
\.


--
-- Data for Name: docs_comment_ffile; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.docs_comment_ffile (id, comment_id, document_id) FROM stdin;
\.


--
-- Data for Name: docs_document; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.docs_document (id, file) FROM stdin;
1	favicon.ico
2	1.png
3	2.png
\.


--
-- Data for Name: docs_metka; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.docs_metka (id, name) FROM stdin;
1	Срочно
2	В будущем
\.


--
-- Data for Name: documents_documentcache; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.documents_documentcache (id, object_type, object_id, action, previous_parent, "timestamp", "full", author_profile_id) FROM stdin;
3		\N		\N	2019-03-02 09:00:02.527406+06	f	125
4		\N		\N	2019-04-10 16:52:34.946905+06	f	133
2	doc	65	cut	-1	2019-02-14 21:04:29.74456+06	t	119
\.


--
-- Data for Name: documents_documentfolder; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.documents_documentfolder (id, title, author_profile_id, parent_id, school_id) FROM stdin;
3	Новая папка3g	119	2	1
2	Новая папка56	119	\N	1
37	Новая папка56	119	\N	2
38	Новая папка38	119	\N	1
39	Новая папка39	119	\N	2
40	Новая папка39	119	37	1
41	Новая папка40	119	\N	2
42	Новая папка41	119	\N	1
43	Новая папка43	119	\N	1
44	Новая папка44	119	\N	1
45	Новая папка45	119	\N	1
46	Новая папка46	119	\N	1
47	Новая папка42	119	\N	2
48	Новая папка48	119	\N	2
49	Новая папка49	119	\N	2
50	Новая папка50	119	\N	2
51	Новая папка51	119	\N	2
52	Новая папка47	119	\N	1
53	8888	133	\N	1
\.


--
-- Data for Name: documents_documentfolder_children; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.documents_documentfolder_children (id, from_documentfolder_id, to_documentfolder_id) FROM stdin;
1	2	3
2	3	2
3	37	40
4	40	37
\.


--
-- Data for Name: documents_documentfolder_files; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.documents_documentfolder_files (id, documentfolder_id, document_id) FROM stdin;
6	2	28
8	37	28
9	2	66
\.


--
-- Data for Name: library_cache; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.library_cache (id, object_type, object_id, action, previous_parent, "timestamp", "full", author_profile_id) FROM stdin;
7	lesson	\N	copy	\N	2019-02-17 11:08:00.528466+06	f	120
6	lesson	45	copy	-1	2019-02-14 20:42:46.322294+06	t	119
8	lesson	\N	copy	\N	2019-03-02 08:59:52.299184+06	f	125
\.


--
-- Data for Name: library_folder; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.library_folder (id, title, author_profile_id, parent_id, school_id) FROM stdin;
41	Новая папка5	119	\N	1
42	Новая папка42	119	\N	2
43	Папка42	119	\N	1
\.


--
-- Data for Name: library_folder_children; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.library_folder_children (id, from_folder_id, to_folder_id) FROM stdin;
\.


--
-- Data for Name: library_folder_lesson_list; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.library_folder_lesson_list (id, folder_id, lesson_id) FROM stdin;
80	41	46
81	41	47
82	42	54
\.


--
-- Data for Name: news_post; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.news_post (id, "timestamp", content, image, height_field, width_field, author_profile_id, school_id) FROM stdin;
16	2019-02-15 02:16:44.82713+06	eded		0	0	119	1
19	2019-02-19 03:36:20.23644+06	nj		0	0	119	2
25	2019-04-10 08:24:34.048711+06	mkmk		0	0	119	1
\.


--
-- Data for Name: papers_comment; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.papers_comment (id, level, "timestamp", content, author_profile_id, lesson_id, parent_id) FROM stdin;
\.


--
-- Data for Name: papers_comment_dislikes; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.papers_comment_dislikes (id, comment_id, profile_id) FROM stdin;
\.


--
-- Data for Name: papers_comment_likes; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.papers_comment_likes (id, comment_id, profile_id) FROM stdin;
\.


--
-- Data for Name: papers_course; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.papers_course (id, title, image, height_field, width_field, content, "timestamp", author_profile_id, cost, stars, rating, school_id) FROM stdin;
6	le		0	0	kl	2019-02-14 22:46:55.681955+06	\N	400	{}	0	1
7	mkmkmk		0	0	mk	2019-02-19 03:44:06.756033+06	\N	4	{}	0	1
8	njrfnj		0	0	nj	2019-02-19 03:44:49.94071+06	119	4	{}	0	1
\.


--
-- Data for Name: papers_course_done_by; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.papers_course_done_by (id, course_id, profile_id) FROM stdin;
\.


--
-- Data for Name: papers_course_lessons; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.papers_course_lessons (id, course_id, lesson_id) FROM stdin;
12	8	45
13	8	48
14	8	49
15	8	53
16	8	51
\.


--
-- Data for Name: papers_course_students; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.papers_course_students (id, course_id, profile_id) FROM stdin;
6	6	119
7	6	120
\.


--
-- Data for Name: papers_lesson; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.papers_lesson (id, title, is_homework, "timestamp", author_profile_id, rating, estimater_ids, grades, school_id, access_to_everyone) FROM stdin;
46	Новый список46	f	2019-02-18 03:30:50.563779+06	119	0	{}	{}	1	f
45	Новая список	f	2019-02-14 20:42:52.29549+06	119	3	{119}	{3}	1	f
47	Новая список	f	2019-02-18 03:42:10.023518+06	119	0	{}	{}	1	f
48	Новый список48	f	2019-02-18 04:15:11.925353+06	119	0	{}	{}	1	f
49	Новый список49	f	2019-02-18 04:15:20.933328+06	119	0	{}	{}	2	f
50	Новый список50	f	2019-02-18 04:16:51.350305+06	119	0	{}	{}	2	f
51	Новый список49	f	2019-02-18 04:16:56.178202+06	119	0	{}	{}	1	f
52	Урок52	f	2019-02-18 21:16:43.989251+06	119	0	{}	{}	1	f
53	Урок51	f	2019-02-18 21:16:52.356609+06	119	0	{}	{}	2	f
54	Урок	f	2019-02-19 04:31:30.381137+06	119	0	{}	{}	1	f
\.


--
-- Data for Name: papers_lesson_done_by; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.papers_lesson_done_by (id, lesson_id, profile_id) FROM stdin;
\.


--
-- Data for Name: papers_lesson_papers; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.papers_lesson_papers (id, lesson_id, paper_id) FROM stdin;
9	45	13
10	45	15
\.


--
-- Data for Name: papers_paper; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.papers_paper (id, title, "timestamp", author_profile_id, typee, school_id) FROM stdin;
13	mk	2019-02-14 22:19:29.237501+06	119	problem	1
14	mk	2019-02-18 03:42:10.04748+06	119	problem	1
15	mkfrfmkl	2019-02-19 03:45:34.508298+06	119	problem	1
\.


--
-- Data for Name: papers_paper_done_by; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.papers_paper_done_by (id, paper_id, profile_id) FROM stdin;
\.


--
-- Data for Name: papers_paper_subthemes; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.papers_paper_subthemes (id, paper_id, subtheme_id) FROM stdin;
28	13	28
29	13	29
30	14	30
31	14	31
32	15	32
\.


--
-- Data for Name: papers_subtheme; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.papers_subtheme (id, content, video, file, youtube_video_link) FROM stdin;
8	njn			
2	nnn			
9	Тест 1			
10	mkd			https://www.youtube.com/embed/204C9yNeOYI
11			p.png	
12				https://www.youtube.com/embed/204C9yNeOYI
13				
14	nnn			
15	Тест 1			
16	mkd			https://www.youtube.com/embed/204C9yNeOYI
17				
18				https://www.youtube.com/embed/204C9yNeOYI
19	njn			
20				
21				
22	Программа — это набор (список) команд. Сначала исполняется первая команда, затем вторая, третья, и так далее. Когда все команды исполнены, программа завершается.\n\n— А какие бывают команды?\n\n— Команды зависят от того, кто их исполняет. Какие команды знает (и понимает) исполнитель.\n\n— Собаке можно дать команду «Сидеть», «Голос», кошке – «Брысь», человеку – «Стоять! Стрелять буду», ну а роботу — «Работай! Работай, твою робомать»			
23				https://www.youtube.com/embed/itgQRal2od0&t=1857s
24				https://www.youtube.com/embed/fB1Su_4oSPM
25				
26	Welcome to the first module of an edX course! Courses on edx.org can be navigated in two general ways. You may wish to follow the designed order of the modules in a course, or you may want to jump around the course in order to get only what you need.\n\nIf you want to move through the course in a linear way, simply continue through the course units by clicking the Next button or swiping left on the edX mobile app. This is important during the first module of a course as it likely includes content related to the syllabus, your instructors, discussion guidelines, and expectations for learners taking the course.\n\nIf you want to skip sections or modules in this course, you have the flexibility to do so. Visit "Course" at the top of this page to see the entire the course at a glance. Use the breadcrumb links to navigate to other parts of the course.			
27	mkmkmkm			
28				
29	mkemd			
30				
31	mkemd			
32				
\.


--
-- Data for Name: papers_subtheme_task_list; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.papers_subtheme_task_list (id, subtheme_id, task_id) FROM stdin;
99	29	60
100	31	61
\.


--
-- Data for Name: schools_cabinet; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.schools_cabinet (id, title, capacity, school_id) FROM stdin;
1	15	15	1
2	A3	0	1
3	2B	0	1
4	xx	0	1
\.


--
-- Data for Name: schools_office; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.schools_office (id, title, address, capacity, school_id) FROM stdin;
1	Алматы	Цв	500	1
\.


--
-- Data for Name: schools_school; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.schools_school (id, title, image_icon, height_field, width_field, image_banner, height_field2, width_field2, content, slogan, new_schedule, official_school) FROM stdin;
2	School2		0	0		0	0			f	f
1	School	None/25846f94304dd77f7a194d69270047a7.jpg	260	325	None/yYroAZX.png	1080	1920	mk	mk	t	f
\.


--
-- Data for Name: schools_subjectage; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.schools_subjectage (id, title, school_id) FROM stdin;
1	1 класс	1
\.


--
-- Data for Name: schools_subjectcategory; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.schools_subjectcategory (id, title, school_id) FROM stdin;
1	Математика	1
2	Физика	1
\.


--
-- Data for Name: squads_squad; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.squads_squad (id, title, slug, image_banner, height_field, width_field, content, slogan, end_date, start_date, image_icon, school_id, color_back) FROM stdin;
19	qwe	qwe		0	0			2019-02-28	2018-10-26		1	
18	mkmk	mkmk		0	0			2019-11-30	2018-10-10		1	#4f20b5
\.


--
-- Data for Name: squads_squad_curator; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.squads_squad_curator (id, squad_id, profile_id) FROM stdin;
26	19	119
27	18	119
\.


--
-- Data for Name: squads_squad_students; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.squads_squad_students (id, squad_id, profile_id) FROM stdin;
24	18	122
26	18	123
27	18	127
29	19	126
31	18	130
32	19	131
33	19	132
34	19	133
35	19	134
36	18	128
37	18	129
38	19	135
39	19	136
40	19	137
41	19	138
42	19	139
43	18	140
44	19	141
45	18	142
\.


--
-- Data for Name: subjects_attendance; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.subjects_attendance (id, present, grade, student_id, subject_id, squad_id, subject_materials_id, teacher_id, school_id) FROM stdin;
3176		-1	128	19	18	1077	119	1
3179		-1	122	19	18	1077	119	1
3181		-1	127	19	18	1077	119	1
3182		-1	123	19	18	1077	119	1
3186		-1	122	19	18	1076	119	1
3188		-1	127	19	18	1076	119	1
3189		-1	123	19	18	1076	119	1
3190		-1	128	19	18	1075	119	1
3193		-1	122	19	18	1075	119	1
3195		-1	127	19	18	1075	119	1
3196		-1	123	19	18	1075	119	1
3197		-1	126	19	19	1077	119	1
3198		-1	126	19	19	1076	119	1
3199		-1	126	19	19	1075	119	1
3782		-1	142	19	18	1079	119	1
3783		-1	140	19	18	1079	119	1
3784		-1	142	19	18	1078	119	1
3867		-1	131	19	19	1081	119	1
3785		-1	140	19	18	1078	119	1
3868		-1	132	19	19	1081	119	1
3200		-1	128	19	18	1078	119	1
3203		-1	122	19	18	1078	119	1
3205		-1	127	19	18	1078	119	1
3206		-1	123	19	18	1078	119	1
3207		-1	128	19	18	1079	119	1
3210		-1	122	19	18	1079	119	1
3212		-1	127	19	18	1079	119	1
3213		-1	123	19	18	1079	119	1
3214		-1	128	19	18	1080	119	1
3217		-1	122	19	18	1080	119	1
3219		-1	127	19	18	1080	119	1
3220		-1	123	19	18	1080	119	1
3221		-1	128	19	18	1081	119	1
3224		-1	122	19	18	1081	119	1
3226		-1	127	19	18	1081	119	1
3227		-1	123	19	18	1081	119	1
3228		-1	128	19	18	1082	119	1
3231		-1	122	19	18	1082	119	1
3233		-1	127	19	18	1082	119	1
3234		-1	123	19	18	1082	119	1
3235		-1	128	19	18	1083	119	1
3238		-1	122	19	18	1083	119	1
3240		-1	127	19	18	1083	119	1
3241		-1	123	19	18	1083	119	1
3786		-1	142	19	18	1077	119	1
3869		-1	133	19	19	1081	119	1
3242		-1	126	19	19	1078	119	1
3870		-1	126	19	19	1081	119	1
3787		-1	140	19	18	1077	119	1
3183	present	3	128	19	18	1076	119	1
3788		-1	142	19	18	1076	119	1
3789		-1	140	19	18	1076	119	1
3840		-1	129	19	18	1081	119	1
3841		-1	142	19	18	1081	119	1
3842		-1	130	19	18	1081	119	1
3843		-1	140	19	18	1081	119	1
3844		-1	142	19	18	1080	119	1
3845		-1	140	19	18	1080	119	1
3847		-1	141	19	19	1080	119	1
3848		-1	138	19	19	1080	119	1
3849		-1	135	19	19	1080	119	1
3850		-1	136	19	19	1080	119	1
3851		-1	139	19	19	1080	119	1
3852		-1	131	19	19	1080	119	1
3853		-1	126	19	19	1080	119	1
3854		-1	134	19	19	1080	119	1
3862		-1	141	19	19	1081	119	1
3863		-1	138	19	19	1081	119	1
3864		-1	135	19	19	1081	119	1
3865		-1	136	19	19	1081	119	1
3866		-1	139	19	19	1081	119	1
3871		-1	134	19	19	1081	119	1
3861	present	-1	137	19	19	1081	119	1
3846	present	5	137	19	19	1080	119	1
3790		-1	142	19	18	1075	119	1
3791		-1	140	19	18	1075	119	1
3855		-1	137	19	19	1075	119	1
3856		-1	141	19	19	1075	119	1
3857		-1	138	19	19	1075	119	1
3858		-1	135	19	19	1075	119	1
3859		-1	136	19	19	1075	119	1
3860		-1	139	19	19	1075	119	1
3792		-1	137	22	19	1145	119	1
3793		-1	141	22	19	1145	119	1
3794		-1	138	22	19	1145	119	1
3795		-1	135	22	19	1145	119	1
3796		-1	136	22	19	1145	119	1
3797		-1	139	22	19	1145	119	1
3798		-1	137	22	19	1144	119	1
3799		-1	141	22	19	1144	119	1
3800		-1	138	22	19	1144	119	1
3801		-1	135	22	19	1144	119	1
3802		-1	136	22	19	1144	119	1
3803		-1	139	22	19	1144	119	1
3804		-1	137	22	19	1146	119	1
3805		-1	141	22	19	1146	119	1
3806		-1	138	22	19	1146	119	1
3807		-1	135	22	19	1146	119	1
3808		-1	136	22	19	1146	119	1
3809		-1	139	22	19	1146	119	1
3810		-1	137	22	19	1147	119	1
3811		-1	141	22	19	1147	119	1
3812		-1	138	22	19	1147	119	1
3813		-1	135	22	19	1147	119	1
3814		-1	136	22	19	1147	119	1
3815		-1	139	22	19	1147	119	1
3816		-1	137	19	19	1079	119	1
3817		-1	141	19	19	1079	119	1
3818		-1	138	19	19	1079	119	1
3570		-1	129	19	18	1078	119	1
3571		-1	129	19	18	1077	119	1
3572		-1	129	19	18	1076	119	1
3573		-1	129	19	18	1075	119	1
3574		-1	129	19	18	1079	119	1
3575		-1	130	19	18	1079	119	1
3576		-1	130	19	18	1078	119	1
3577		-1	130	19	18	1077	119	1
3578		-1	130	19	18	1076	119	1
3608		-1	130	19	18	1075	119	1
3819		-1	135	19	19	1079	119	1
3820		-1	136	19	19	1079	119	1
3821		-1	139	19	19	1079	119	1
3822		-1	137	19	19	1078	119	1
3823		-1	141	19	19	1078	119	1
3824		-1	138	19	19	1078	119	1
3825		-1	135	19	19	1078	119	1
3826		-1	136	19	19	1078	119	1
3827		-1	139	19	19	1078	119	1
3828		-1	137	19	19	1077	119	1
3829		-1	141	19	19	1077	119	1
3830		-1	138	19	19	1077	119	1
3831		-1	135	19	19	1077	119	1
3832		-1	136	19	19	1077	119	1
3833		-1	139	19	19	1077	119	1
3834		-1	137	19	19	1076	119	1
3835		-1	141	19	19	1076	119	1
3836		-1	138	19	19	1076	119	1
3837		-1	135	19	19	1076	119	1
3838		-1	136	19	19	1076	119	1
3839		-1	139	19	19	1076	119	1
3663		-1	129	19	18	1080	119	1
3664		-1	130	19	18	1080	119	1
3665		-1	131	19	19	1079	119	1
3666		-1	132	19	19	1079	119	1
3667		-1	126	19	19	1079	119	1
3668		-1	131	19	19	1078	119	1
3670		-1	131	19	19	1077	119	1
3671		-1	132	19	19	1077	119	1
3672		-1	131	19	19	1076	119	1
3673		-1	132	19	19	1076	119	1
3669	present	5	132	19	19	1078	119	1
3701		-1	131	19	19	1075	119	1
3702		-1	132	19	19	1075	119	1
3703		-1	132	19	19	1080	119	1
3705		-1	133	19	19	1080	119	1
3706		-1	133	19	19	1079	119	1
3707		-1	133	19	19	1078	119	1
3708		-1	133	19	19	1077	119	1
3713		-1	133	19	19	1076	119	1
3714		-1	133	19	19	1075	119	1
3745		-1	131	22	19	1145	119	1
3746		-1	132	22	19	1145	119	1
3747		-1	133	22	19	1145	119	1
3748		-1	126	22	19	1145	119	1
3749		-1	134	22	19	1145	119	1
3750		-1	131	22	19	1144	119	1
3751		-1	132	22	19	1144	119	1
3752		-1	133	22	19	1144	119	1
3753		-1	126	22	19	1144	119	1
3754		-1	134	22	19	1144	119	1
3755		-1	131	22	19	1146	119	1
3756		-1	132	22	19	1146	119	1
3757		-1	133	22	19	1146	119	1
3758		-1	126	22	19	1146	119	1
3759		-1	134	22	19	1146	119	1
3760		-1	131	22	19	1147	119	1
3761		-1	132	22	19	1147	119	1
3762		-1	133	22	19	1147	119	1
3763		-1	126	22	19	1147	119	1
3764		-1	134	22	19	1147	119	1
3777		-1	134	19	19	1079	119	1
3778		-1	134	19	19	1078	119	1
3779		-1	134	19	19	1077	119	1
3780		-1	134	19	19	1076	119	1
3781		-1	134	19	19	1075	119	1
\.


--
-- Data for Name: subjects_cacheattendance; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.subjects_cacheattendance (id, profile_id, squad_id, subject_id) FROM stdin;
14	131	\N	\N
15	132	19	19
16	133	19	19
17	119	19	19
12	120	\N	\N
\.


--
-- Data for Name: subjects_cell; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.subjects_cell (id, day_id, time_period_id, school_id) FROM stdin;
22	1	1	1
23	1	2	1
24	1	3	1
25	2	1	1
26	2	2	1
27	2	3	1
28	3	1	1
29	3	2	1
30	3	3	1
31	4	1	1
32	4	2	1
33	4	3	1
34	5	1	1
35	5	2	1
36	5	3	1
37	6	1	1
38	6	2	1
39	6	3	1
40	7	1	1
41	7	2	1
42	7	3	1
\.


--
-- Data for Name: subjects_day; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.subjects_day (id, title, number) FROM stdin;
1	Пн	1
2	Вт	2
3	Ср	3
4	ЧТ	4
5	ПТ	5
6	Сб	6
7	Вс	7
\.


--
-- Data for Name: subjects_lecture; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.subjects_lecture (id, cell_id, squad_id, subject_id, school_id, cabinet_id, day_id, age_id, category_id, office_id) FROM stdin;
244	22	18	19	1	\N	1	1	1	1
257	26	19	22	1	\N	2	\N	\N	\N
258	36	19	22	1	\N	4	1	1	1
245	26	19	19	1	\N	2	1	1	1
\.


--
-- Data for Name: subjects_lecture_people; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.subjects_lecture_people (id, lecture_id, profile_id) FROM stdin;
243	245	135
244	257	135
245	258	135
246	245	136
247	257	136
248	258	136
249	245	137
250	257	137
251	258	137
252	245	138
253	257	138
254	258	138
255	245	139
256	257	139
257	258	139
258	244	140
259	245	141
260	257	141
151	244	128
152	244	120
153	244	121
154	244	122
155	244	123
156	244	124
157	244	127
158	244	119
159	245	126
160	245	119
261	258	141
262	244	142
225	245	131
228	245	132
231	245	133
234	245	134
237	258	131
238	258	132
239	258	133
240	258	134
241	258	126
242	258	119
\.


--
-- Data for Name: subjects_subject; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.subjects_subject (id, title, slug, image_banner, height_field, width_field, content, slogan, start_date, end_date, number_of_lectures, image_icon, height_field2, height_field3, image_back, width_field2, width_field3, color_back, school_id, age_id, category_id, office_id, cost, squad_ids, start_dates) FROM stdin;
22	new s	qqq22	22/dark.png	602	1070	mm	dd	2019-04-09	2019-05-11	10	22/dark.png	602	602	22/dark.png	1070	1070	red	1	1	1	1	500	{19}	{2019-04-09}
19	Qwer	0		602	1070	mk	mk	2019-03-01	2019-04-30	9	19/dark.png	0	0		0	0	red	1	1	1	1	5000	{18,19}	{2019-03-04,2019-03-05}
\.


--
-- Data for Name: subjects_subject_squads; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.subjects_subject_squads (id, subject_id, squad_id) FROM stdin;
64	19	18
65	19	19
70	22	19
\.


--
-- Data for Name: subjects_subject_students; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.subjects_subject_students (id, subject_id, profile_id) FROM stdin;
325	22	131
326	22	132
327	22	133
328	22	126
329	22	134
360	19	128
361	19	129
362	19	130
363	19	122
364	19	123
365	19	127
366	19	135
303	19	133
367	22	135
368	19	136
369	22	136
370	19	137
371	22	137
372	19	138
373	22	138
374	19	139
375	22	139
376	19	140
377	19	141
378	22	141
379	19	142
\.


--
-- Data for Name: subjects_subject_teacher; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.subjects_subject_teacher (id, subject_id, profile_id) FROM stdin;
146	19	119
149	22	119
\.


--
-- Data for Name: subjects_subjectmaterials; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.subjects_subjectmaterials (id, number, subject_id, school_id) FROM stdin;
1075	1	19	1
1076	2	19	1
1077	3	19	1
1078	4	19	1
1079	5	19	1
1080	6	19	1
1081	7	19	1
1082	8	19	1
1083	9	19	1
1144	1	22	1
1145	2	22	1
1146	3	22	1
1147	4	22	1
1148	5	22	1
1149	6	22	1
1150	7	22	1
1151	8	22	1
1152	9	22	1
1153	10	22	1
\.


--
-- Data for Name: subjects_subjectmaterials_done_by; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.subjects_subjectmaterials_done_by (id, subjectmaterials_id, profile_id) FROM stdin;
\.


--
-- Data for Name: subjects_subjectmaterials_lessons; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.subjects_subjectmaterials_lessons (id, subjectmaterials_id, lesson_id) FROM stdin;
33	1075	45
34	1080	45
\.


--
-- Data for Name: subjects_timeperiod; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.subjects_timeperiod (id, start, "end", num, school_id) FROM stdin;
2	2:03	5:00	2	1
3	13:05	17:00	3	1
1	1:01	2:00	1	1
\.


--
-- Data for Name: subjects_timeperiod_people; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.subjects_timeperiod_people (id, timeperiod_id, profile_id) FROM stdin;
1	1	119
2	1	120
3	1	121
4	1	122
5	1	123
6	1	124
7	2	119
8	2	120
9	2	121
10	2	122
11	2	123
12	2	124
13	3	119
14	3	120
15	3	121
16	3	122
17	3	123
18	3	124
19	1	128
20	1	125
21	1	126
22	1	127
23	2	128
24	2	125
25	2	126
26	2	127
27	3	128
28	3	125
29	3	126
30	3	127
31	1	132
32	2	132
33	3	132
34	1	133
35	2	133
36	3	133
37	1	134
38	2	134
39	3	134
40	1	135
41	2	135
42	3	135
43	1	136
44	2	136
45	3	136
46	1	137
47	2	137
48	3	137
49	1	138
50	2	138
51	3	138
52	1	139
53	2	139
54	3	139
55	1	140
56	2	140
57	3	140
58	1	141
59	2	141
60	3	141
61	1	142
62	2	142
63	3	142
\.


--
-- Data for Name: tasks_problemtag; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.tasks_problemtag (id, title) FROM stdin;
1	Алгебра
2	Геометрия
3	Физика
4	Химия
5	1й
6	1йк
7	n
8	rew
9	ггг
10	еее
11	4
12	4kmk
13	55
14	m
\.


--
-- Data for Name: tasks_solver; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.tasks_solver (id, solver_ans, solver_correctness, solver_try_number, author_profile_id, task_id) FROM stdin;
34	{""}	f	0	119	60
35	{}	f	0	125	60
\.


--
-- Data for Name: tasks_task; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.tasks_task (id, slug, text, image, height_field, width_field, answer, cost, is_test, is_mult_ans, variants, author_profile_id, parent_id) FROM stdin;
61	qqq61	mkmkmkmk		0	0	{4}	1	f	f	{}	119	\N
60	0	Одно трехзначное число состоит из различных цифр, следующих в порядке возрастания, а в его названии все слова начинаются с одной и той же буквы. Другое трехзначное число, наоборот, состоит из одинаковых цифр, но в его названии все слова начинаются с разных букв. Какие это числа?		0	0	{4}	5	f	f	{""}	119	\N
\.


--
-- Data for Name: tasks_task_tags; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.tasks_task_tags (id, task_id, problemtag_id) FROM stdin;
15	60	14
\.


--
-- Data for Name: todolist_board; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.todolist_board (id, name, school_id) FROM stdin;
1	jnj	1
2	jnjn	1
\.


--
-- Data for Name: todolist_card; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.todolist_card (id, title, slug, description, column_id) FROM stdin;
6	njn	njn		4
7	qqq	qqq		3
5	cdd	cdd		1
\.


--
-- Data for Name: todolist_card_doc_list; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.todolist_card_doc_list (id, card_id, document_id) FROM stdin;
\.


--
-- Data for Name: todolist_card_metka_list; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.todolist_card_metka_list (id, card_id, metka_id) FROM stdin;
\.


--
-- Data for Name: todolist_card_user_list; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.todolist_card_user_list (id, card_id, profile_id) FROM stdin;
\.


--
-- Data for Name: todolist_column; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.todolist_column (id, title, board_id) FROM stdin;
1	nn	1
2	jjj	1
3	nj	2
4	nnnn	2
\.


--
-- Data for Name: todolist_comment; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.todolist_comment (id, content, "timestamp", image, height_field, width_field, author_profile_id, card_id) FROM stdin;
\.


--
-- Data for Name: todolist_comment_ffile; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.todolist_comment_ffile (id, comment_id, document_id) FROM stdin;
\.


--
-- Data for Name: todolist_document; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.todolist_document (id, file, object_type, school_id) FROM stdin;
6	p.png	img	1
7	Pinocchio.pdf	pdf	1
24	admin.py	html	1
27	Pinocchio.pdf	pdf	1
28	p.png	img	1
30	p.png	img	2
63	Pinocchio.pdf	pdf	2
64	dark.png		1
65	dark.png	img	1
66	dark.png	img	1
\.


--
-- Data for Name: todolist_metka; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.todolist_metka (id, name) FROM stdin;
\.


--
-- Name: accounts_corruption_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.accounts_corruption_id_seq', 8, true);


--
-- Name: accounts_crmcard_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.accounts_crmcard_id_seq', 8, true);


--
-- Name: accounts_crmcolumn_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.accounts_crmcolumn_id_seq', 4, true);


--
-- Name: accounts_jobcategory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.accounts_jobcategory_id_seq', 2, true);


--
-- Name: accounts_misslesson_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.accounts_misslesson_id_seq', 20, true);


--
-- Name: accounts_profession_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.accounts_profession_id_seq', 8, true);


--
-- Name: accounts_profile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.accounts_profile_id_seq', 142, true);


--
-- Name: accounts_profile_job_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.accounts_profile_job_categories_id_seq', 4, true);


--
-- Name: accounts_profile_profession_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.accounts_profile_profession_id_seq', 30, true);


--
-- Name: accounts_profile_schools_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.accounts_profile_schools_id_seq', 29, true);


--
-- Name: accounts_zaiavka_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.accounts_zaiavka_id_seq', 1, true);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 263, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 117, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1754, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 68, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 236, true);


--
-- Name: docs_board_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.docs_board_id_seq', 3, true);


--
-- Name: docs_card_doc_list_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.docs_card_doc_list_id_seq', 1, true);


--
-- Name: docs_card_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.docs_card_id_seq', 5, true);


--
-- Name: docs_card_metka_list_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.docs_card_metka_list_id_seq', 2, true);


--
-- Name: docs_card_user_list_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.docs_card_user_list_id_seq', 17, true);


--
-- Name: docs_column_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.docs_column_id_seq', 6, true);


--
-- Name: docs_comment_ffile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.docs_comment_ffile_id_seq', 1, false);


--
-- Name: docs_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.docs_comment_id_seq', 1, true);


--
-- Name: docs_document_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.docs_document_id_seq', 3, true);


--
-- Name: docs_metka_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.docs_metka_id_seq', 2, true);


--
-- Name: documents_documentcache_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.documents_documentcache_id_seq', 4, true);


--
-- Name: documents_documentfolder_children_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.documents_documentfolder_children_id_seq', 4, true);


--
-- Name: documents_documentfolder_files_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.documents_documentfolder_files_id_seq', 9, true);


--
-- Name: documents_documentfolder_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.documents_documentfolder_id_seq', 53, true);


--
-- Name: library_cache_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.library_cache_id_seq', 8, true);


--
-- Name: library_folder_children_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.library_folder_children_id_seq', 64, true);


--
-- Name: library_folder_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.library_folder_id_seq', 43, true);


--
-- Name: library_folder_lesson_list_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.library_folder_lesson_list_id_seq', 82, true);


--
-- Name: news_post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.news_post_id_seq', 25, true);


--
-- Name: papers_comment_dislikes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.papers_comment_dislikes_id_seq', 25, true);


--
-- Name: papers_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.papers_comment_id_seq', 17, true);


--
-- Name: papers_comment_likes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.papers_comment_likes_id_seq', 26, true);


--
-- Name: papers_course_done_by_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.papers_course_done_by_id_seq', 1, true);


--
-- Name: papers_course_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.papers_course_id_seq', 8, true);


--
-- Name: papers_course_lesson_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.papers_course_lesson_id_seq', 16, true);


--
-- Name: papers_course_students_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.papers_course_students_id_seq', 7, true);


--
-- Name: papers_lesson_done_by_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.papers_lesson_done_by_id_seq', 2, true);


--
-- Name: papers_lesson_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.papers_lesson_id_seq', 54, true);


--
-- Name: papers_lesson_papers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.papers_lesson_papers_id_seq', 10, true);


--
-- Name: papers_paper_done_by_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.papers_paper_done_by_id_seq', 15, true);


--
-- Name: papers_paper_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.papers_paper_id_seq', 15, true);


--
-- Name: papers_paper_subthemes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.papers_paper_subthemes_id_seq', 32, true);


--
-- Name: papers_subtheme_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.papers_subtheme_id_seq', 32, true);


--
-- Name: papers_subtheme_task_list_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.papers_subtheme_task_list_id_seq', 100, true);


--
-- Name: schools_cabinett_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.schools_cabinett_id_seq', 4, true);


--
-- Name: schools_office_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.schools_office_id_seq', 1, true);


--
-- Name: schools_school_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.schools_school_id_seq', 2, true);


--
-- Name: schools_subjectage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.schools_subjectage_id_seq', 1, true);


--
-- Name: schools_subjectcategory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.schools_subjectcategory_id_seq', 2, true);


--
-- Name: squads_squad_curator_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.squads_squad_curator_id_seq', 27, true);


--
-- Name: squads_squad_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.squads_squad_id_seq', 19, true);


--
-- Name: squads_squad_students_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.squads_squad_students_id_seq', 45, true);


--
-- Name: subjects_attendance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.subjects_attendance_id_seq', 3871, true);


--
-- Name: subjects_cacheattendance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.subjects_cacheattendance_id_seq', 17, true);


--
-- Name: subjects_cell_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.subjects_cell_id_seq', 42, true);


--
-- Name: subjects_day_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.subjects_day_id_seq', 7, true);


--
-- Name: subjects_lecture_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.subjects_lecture_id_seq', 258, true);


--
-- Name: subjects_lecture_people_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.subjects_lecture_people_id_seq', 262, true);


--
-- Name: subjects_subject_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.subjects_subject_id_seq', 22, true);


--
-- Name: subjects_subject_squads_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.subjects_subject_squads_id_seq', 70, true);


--
-- Name: subjects_subject_students_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.subjects_subject_students_id_seq', 379, true);


--
-- Name: subjects_subject_teacher_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.subjects_subject_teacher_id_seq', 149, true);


--
-- Name: subjects_subjectmaterials_done_by_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.subjects_subjectmaterials_done_by_id_seq', 1, false);


--
-- Name: subjects_subjectmaterials_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.subjects_subjectmaterials_id_seq', 1153, true);


--
-- Name: subjects_subjectmaterials_lessons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.subjects_subjectmaterials_lessons_id_seq', 34, true);


--
-- Name: subjects_timeperiod_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.subjects_timeperiod_id_seq', 3, true);


--
-- Name: subjects_timeperiod_students_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.subjects_timeperiod_students_id_seq', 63, true);


--
-- Name: tasks_problemtag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.tasks_problemtag_id_seq', 14, true);


--
-- Name: tasks_solver_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.tasks_solver_id_seq', 35, true);


--
-- Name: tasks_task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.tasks_task_id_seq', 61, true);


--
-- Name: tasks_task_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.tasks_task_tags_id_seq', 15, true);


--
-- Name: todolist_board_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.todolist_board_id_seq', 2, true);


--
-- Name: todolist_card_doc_list_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.todolist_card_doc_list_id_seq', 1, false);


--
-- Name: todolist_card_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.todolist_card_id_seq', 7, true);


--
-- Name: todolist_card_metka_list_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.todolist_card_metka_list_id_seq', 1, false);


--
-- Name: todolist_card_user_list_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.todolist_card_user_list_id_seq', 3, true);


--
-- Name: todolist_column_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.todolist_column_id_seq', 4, true);


--
-- Name: todolist_comment_ffile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.todolist_comment_ffile_id_seq', 1, false);


--
-- Name: todolist_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.todolist_comment_id_seq', 1, true);


--
-- Name: todolist_document_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.todolist_document_id_seq', 66, true);


--
-- Name: todolist_metka_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.todolist_metka_id_seq', 1, false);


--
-- Name: accounts_corruption accounts_corruption_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_corruption
    ADD CONSTRAINT accounts_corruption_pkey PRIMARY KEY (id);


--
-- Name: accounts_crmcard accounts_crmcard_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_crmcard
    ADD CONSTRAINT accounts_crmcard_pkey PRIMARY KEY (id);


--
-- Name: accounts_crmcolumn accounts_crmcolumn_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_crmcolumn
    ADD CONSTRAINT accounts_crmcolumn_pkey PRIMARY KEY (id);


--
-- Name: accounts_jobcategory accounts_jobcategory_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_jobcategory
    ADD CONSTRAINT accounts_jobcategory_pkey PRIMARY KEY (id);


--
-- Name: accounts_misslesson accounts_misslesson_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_misslesson
    ADD CONSTRAINT accounts_misslesson_pkey PRIMARY KEY (id);


--
-- Name: accounts_misslesson accounts_misslesson_profile_id_fca77b26_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_misslesson
    ADD CONSTRAINT accounts_misslesson_profile_id_fca77b26_uniq UNIQUE (profile_id);


--
-- Name: accounts_profession accounts_profession_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profession
    ADD CONSTRAINT accounts_profession_pkey PRIMARY KEY (id);


--
-- Name: accounts_profile_job_categories accounts_profile_job_cat_profile_id_jobcategory_i_3b41a24d_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profile_job_categories
    ADD CONSTRAINT accounts_profile_job_cat_profile_id_jobcategory_i_3b41a24d_uniq UNIQUE (profile_id, jobcategory_id);


--
-- Name: accounts_profile_job_categories accounts_profile_job_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profile_job_categories
    ADD CONSTRAINT accounts_profile_job_categories_pkey PRIMARY KEY (id);


--
-- Name: accounts_profile accounts_profile_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profile
    ADD CONSTRAINT accounts_profile_pkey PRIMARY KEY (id);


--
-- Name: accounts_profile_profession accounts_profile_profess_profile_id_profession_id_f86ebbc7_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profile_profession
    ADD CONSTRAINT accounts_profile_profess_profile_id_profession_id_f86ebbc7_uniq UNIQUE (profile_id, profession_id);


--
-- Name: accounts_profile_profession accounts_profile_profession_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profile_profession
    ADD CONSTRAINT accounts_profile_profession_pkey PRIMARY KEY (id);


--
-- Name: accounts_profile_schools accounts_profile_schools_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profile_schools
    ADD CONSTRAINT accounts_profile_schools_pkey PRIMARY KEY (id);


--
-- Name: accounts_profile_schools accounts_profile_schools_profile_id_school_id_a746c9fb_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profile_schools
    ADD CONSTRAINT accounts_profile_schools_profile_id_school_id_a746c9fb_uniq UNIQUE (profile_id, school_id);


--
-- Name: accounts_profile accounts_profile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profile
    ADD CONSTRAINT accounts_profile_user_id_key UNIQUE (user_id);


--
-- Name: accounts_zaiavka accounts_zaiavka_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_zaiavka
    ADD CONSTRAINT accounts_zaiavka_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: docs_board docs_board_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_board
    ADD CONSTRAINT docs_board_pkey PRIMARY KEY (id);


--
-- Name: docs_card_doc_list docs_card_doc_list_card_id_document_id_3c40f2b2_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_card_doc_list
    ADD CONSTRAINT docs_card_doc_list_card_id_document_id_3c40f2b2_uniq UNIQUE (card_id, document_id);


--
-- Name: docs_card_doc_list docs_card_doc_list_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_card_doc_list
    ADD CONSTRAINT docs_card_doc_list_pkey PRIMARY KEY (id);


--
-- Name: docs_card_metka_list docs_card_metka_list_card_id_metka_id_03ed00d1_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_card_metka_list
    ADD CONSTRAINT docs_card_metka_list_card_id_metka_id_03ed00d1_uniq UNIQUE (card_id, metka_id);


--
-- Name: docs_card_metka_list docs_card_metka_list_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_card_metka_list
    ADD CONSTRAINT docs_card_metka_list_pkey PRIMARY KEY (id);


--
-- Name: docs_card docs_card_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_card
    ADD CONSTRAINT docs_card_pkey PRIMARY KEY (id);


--
-- Name: docs_card_user_list docs_card_user_list_card_id_profile_id_8707489f_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_card_user_list
    ADD CONSTRAINT docs_card_user_list_card_id_profile_id_8707489f_uniq UNIQUE (card_id, profile_id);


--
-- Name: docs_card_user_list docs_card_user_list_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_card_user_list
    ADD CONSTRAINT docs_card_user_list_pkey PRIMARY KEY (id);


--
-- Name: docs_column docs_column_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_column
    ADD CONSTRAINT docs_column_pkey PRIMARY KEY (id);


--
-- Name: docs_comment_ffile docs_comment_ffile_comment_id_document_id_50c94dc4_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_comment_ffile
    ADD CONSTRAINT docs_comment_ffile_comment_id_document_id_50c94dc4_uniq UNIQUE (comment_id, document_id);


--
-- Name: docs_comment_ffile docs_comment_ffile_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_comment_ffile
    ADD CONSTRAINT docs_comment_ffile_pkey PRIMARY KEY (id);


--
-- Name: docs_comment docs_comment_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_comment
    ADD CONSTRAINT docs_comment_pkey PRIMARY KEY (id);


--
-- Name: docs_document docs_document_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_document
    ADD CONSTRAINT docs_document_pkey PRIMARY KEY (id);


--
-- Name: docs_metka docs_metka_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_metka
    ADD CONSTRAINT docs_metka_pkey PRIMARY KEY (id);


--
-- Name: documents_documentcache documents_documentcache_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.documents_documentcache
    ADD CONSTRAINT documents_documentcache_pkey PRIMARY KEY (id);


--
-- Name: documents_documentfolder_children documents_documentfolder_children_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.documents_documentfolder_children
    ADD CONSTRAINT documents_documentfolder_children_pkey PRIMARY KEY (id);


--
-- Name: documents_documentfolder_files documents_documentfolder_documentfolder_id_docume_90584034_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.documents_documentfolder_files
    ADD CONSTRAINT documents_documentfolder_documentfolder_id_docume_90584034_uniq UNIQUE (documentfolder_id, document_id);


--
-- Name: documents_documentfolder_files documents_documentfolder_files_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.documents_documentfolder_files
    ADD CONSTRAINT documents_documentfolder_files_pkey PRIMARY KEY (id);


--
-- Name: documents_documentfolder_children documents_documentfolder_from_documentfolder_id_t_be89f29c_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.documents_documentfolder_children
    ADD CONSTRAINT documents_documentfolder_from_documentfolder_id_t_be89f29c_uniq UNIQUE (from_documentfolder_id, to_documentfolder_id);


--
-- Name: documents_documentfolder documents_documentfolder_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.documents_documentfolder
    ADD CONSTRAINT documents_documentfolder_pkey PRIMARY KEY (id);


--
-- Name: library_cache library_cache_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.library_cache
    ADD CONSTRAINT library_cache_pkey PRIMARY KEY (id);


--
-- Name: library_folder_children library_folder_children_from_folder_id_to_folder_db56e45c_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.library_folder_children
    ADD CONSTRAINT library_folder_children_from_folder_id_to_folder_db56e45c_uniq UNIQUE (from_folder_id, to_folder_id);


--
-- Name: library_folder_children library_folder_children_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.library_folder_children
    ADD CONSTRAINT library_folder_children_pkey PRIMARY KEY (id);


--
-- Name: library_folder_lesson_list library_folder_lesson_list_folder_id_lesson_id_452f4e2a_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.library_folder_lesson_list
    ADD CONSTRAINT library_folder_lesson_list_folder_id_lesson_id_452f4e2a_uniq UNIQUE (folder_id, lesson_id);


--
-- Name: library_folder_lesson_list library_folder_lesson_list_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.library_folder_lesson_list
    ADD CONSTRAINT library_folder_lesson_list_pkey PRIMARY KEY (id);


--
-- Name: library_folder library_folder_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.library_folder
    ADD CONSTRAINT library_folder_pkey PRIMARY KEY (id);


--
-- Name: news_post news_post_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.news_post
    ADD CONSTRAINT news_post_pkey PRIMARY KEY (id);


--
-- Name: papers_comment_dislikes papers_comment_dislikes_comment_id_profile_id_a4893e14_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_comment_dislikes
    ADD CONSTRAINT papers_comment_dislikes_comment_id_profile_id_a4893e14_uniq UNIQUE (comment_id, profile_id);


--
-- Name: papers_comment_dislikes papers_comment_dislikes_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_comment_dislikes
    ADD CONSTRAINT papers_comment_dislikes_pkey PRIMARY KEY (id);


--
-- Name: papers_comment_likes papers_comment_likes_comment_id_profile_id_fecc32bd_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_comment_likes
    ADD CONSTRAINT papers_comment_likes_comment_id_profile_id_fecc32bd_uniq UNIQUE (comment_id, profile_id);


--
-- Name: papers_comment_likes papers_comment_likes_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_comment_likes
    ADD CONSTRAINT papers_comment_likes_pkey PRIMARY KEY (id);


--
-- Name: papers_comment papers_comment_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_comment
    ADD CONSTRAINT papers_comment_pkey PRIMARY KEY (id);


--
-- Name: papers_course_done_by papers_course_done_by_course_id_profile_id_083520ec_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_course_done_by
    ADD CONSTRAINT papers_course_done_by_course_id_profile_id_083520ec_uniq UNIQUE (course_id, profile_id);


--
-- Name: papers_course_done_by papers_course_done_by_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_course_done_by
    ADD CONSTRAINT papers_course_done_by_pkey PRIMARY KEY (id);


--
-- Name: papers_course_lessons papers_course_lesson_course_id_lesson_id_25c8f694_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_course_lessons
    ADD CONSTRAINT papers_course_lesson_course_id_lesson_id_25c8f694_uniq UNIQUE (course_id, lesson_id);


--
-- Name: papers_course_lessons papers_course_lesson_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_course_lessons
    ADD CONSTRAINT papers_course_lesson_pkey PRIMARY KEY (id);


--
-- Name: papers_course papers_course_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_course
    ADD CONSTRAINT papers_course_pkey PRIMARY KEY (id);


--
-- Name: papers_course_students papers_course_students_course_id_profile_id_b2090d55_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_course_students
    ADD CONSTRAINT papers_course_students_course_id_profile_id_b2090d55_uniq UNIQUE (course_id, profile_id);


--
-- Name: papers_course_students papers_course_students_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_course_students
    ADD CONSTRAINT papers_course_students_pkey PRIMARY KEY (id);


--
-- Name: papers_lesson_done_by papers_lesson_done_by_lesson_id_profile_id_2428a190_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_lesson_done_by
    ADD CONSTRAINT papers_lesson_done_by_lesson_id_profile_id_2428a190_uniq UNIQUE (lesson_id, profile_id);


--
-- Name: papers_lesson_done_by papers_lesson_done_by_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_lesson_done_by
    ADD CONSTRAINT papers_lesson_done_by_pkey PRIMARY KEY (id);


--
-- Name: papers_lesson_papers papers_lesson_papers_lesson_id_paper_id_5a6e6c6c_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_lesson_papers
    ADD CONSTRAINT papers_lesson_papers_lesson_id_paper_id_5a6e6c6c_uniq UNIQUE (lesson_id, paper_id);


--
-- Name: papers_lesson_papers papers_lesson_papers_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_lesson_papers
    ADD CONSTRAINT papers_lesson_papers_pkey PRIMARY KEY (id);


--
-- Name: papers_lesson papers_lesson_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_lesson
    ADD CONSTRAINT papers_lesson_pkey PRIMARY KEY (id);


--
-- Name: papers_paper_done_by papers_paper_done_by_paper_id_profile_id_2fa7b871_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_paper_done_by
    ADD CONSTRAINT papers_paper_done_by_paper_id_profile_id_2fa7b871_uniq UNIQUE (paper_id, profile_id);


--
-- Name: papers_paper_done_by papers_paper_done_by_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_paper_done_by
    ADD CONSTRAINT papers_paper_done_by_pkey PRIMARY KEY (id);


--
-- Name: papers_paper papers_paper_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_paper
    ADD CONSTRAINT papers_paper_pkey PRIMARY KEY (id);


--
-- Name: papers_paper_subthemes papers_paper_subthemes_paper_id_subtheme_id_54c40014_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_paper_subthemes
    ADD CONSTRAINT papers_paper_subthemes_paper_id_subtheme_id_54c40014_uniq UNIQUE (paper_id, subtheme_id);


--
-- Name: papers_paper_subthemes papers_paper_subthemes_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_paper_subthemes
    ADD CONSTRAINT papers_paper_subthemes_pkey PRIMARY KEY (id);


--
-- Name: papers_subtheme papers_subtheme_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_subtheme
    ADD CONSTRAINT papers_subtheme_pkey PRIMARY KEY (id);


--
-- Name: papers_subtheme_task_list papers_subtheme_task_list_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_subtheme_task_list
    ADD CONSTRAINT papers_subtheme_task_list_pkey PRIMARY KEY (id);


--
-- Name: papers_subtheme_task_list papers_subtheme_task_list_subtheme_id_task_id_cf1d4b2c_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_subtheme_task_list
    ADD CONSTRAINT papers_subtheme_task_list_subtheme_id_task_id_cf1d4b2c_uniq UNIQUE (subtheme_id, task_id);


--
-- Name: schools_cabinet schools_cabinett_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schools_cabinet
    ADD CONSTRAINT schools_cabinett_pkey PRIMARY KEY (id);


--
-- Name: schools_office schools_office_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schools_office
    ADD CONSTRAINT schools_office_pkey PRIMARY KEY (id);


--
-- Name: schools_school schools_school_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schools_school
    ADD CONSTRAINT schools_school_pkey PRIMARY KEY (id);


--
-- Name: schools_subjectage schools_subjectage_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schools_subjectage
    ADD CONSTRAINT schools_subjectage_pkey PRIMARY KEY (id);


--
-- Name: schools_subjectcategory schools_subjectcategory_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schools_subjectcategory
    ADD CONSTRAINT schools_subjectcategory_pkey PRIMARY KEY (id);


--
-- Name: squads_squad_curator squads_squad_curator_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.squads_squad_curator
    ADD CONSTRAINT squads_squad_curator_pkey PRIMARY KEY (id);


--
-- Name: squads_squad_curator squads_squad_curator_squad_id_profile_id_d7edd33e_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.squads_squad_curator
    ADD CONSTRAINT squads_squad_curator_squad_id_profile_id_d7edd33e_uniq UNIQUE (squad_id, profile_id);


--
-- Name: squads_squad squads_squad_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.squads_squad
    ADD CONSTRAINT squads_squad_pkey PRIMARY KEY (id);


--
-- Name: squads_squad squads_squad_slug_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.squads_squad
    ADD CONSTRAINT squads_squad_slug_key UNIQUE (slug);


--
-- Name: squads_squad_students squads_squad_students_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.squads_squad_students
    ADD CONSTRAINT squads_squad_students_pkey PRIMARY KEY (id);


--
-- Name: squads_squad_students squads_squad_students_squad_id_profile_id_9b8cb54d_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.squads_squad_students
    ADD CONSTRAINT squads_squad_students_squad_id_profile_id_9b8cb54d_uniq UNIQUE (squad_id, profile_id);


--
-- Name: subjects_attendance subjects_attendance_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_attendance
    ADD CONSTRAINT subjects_attendance_pkey PRIMARY KEY (id);


--
-- Name: subjects_cacheattendance subjects_cacheattendance_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_cacheattendance
    ADD CONSTRAINT subjects_cacheattendance_pkey PRIMARY KEY (id);


--
-- Name: subjects_cacheattendance subjects_cacheattendance_profile_id_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_cacheattendance
    ADD CONSTRAINT subjects_cacheattendance_profile_id_key UNIQUE (profile_id);


--
-- Name: subjects_cell subjects_cell_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_cell
    ADD CONSTRAINT subjects_cell_pkey PRIMARY KEY (id);


--
-- Name: subjects_day subjects_day_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_day
    ADD CONSTRAINT subjects_day_pkey PRIMARY KEY (id);


--
-- Name: subjects_lecture_people subjects_lecture_people_lecture_id_profile_id_56c8e8b0_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_lecture_people
    ADD CONSTRAINT subjects_lecture_people_lecture_id_profile_id_56c8e8b0_uniq UNIQUE (lecture_id, profile_id);


--
-- Name: subjects_lecture_people subjects_lecture_people_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_lecture_people
    ADD CONSTRAINT subjects_lecture_people_pkey PRIMARY KEY (id);


--
-- Name: subjects_lecture subjects_lecture_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_lecture
    ADD CONSTRAINT subjects_lecture_pkey PRIMARY KEY (id);


--
-- Name: subjects_subject subjects_subject_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subject
    ADD CONSTRAINT subjects_subject_pkey PRIMARY KEY (id);


--
-- Name: subjects_subject subjects_subject_slug_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subject
    ADD CONSTRAINT subjects_subject_slug_key UNIQUE (slug);


--
-- Name: subjects_subject_squads subjects_subject_squads_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subject_squads
    ADD CONSTRAINT subjects_subject_squads_pkey PRIMARY KEY (id);


--
-- Name: subjects_subject_squads subjects_subject_squads_subject_id_squad_id_20b4127f_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subject_squads
    ADD CONSTRAINT subjects_subject_squads_subject_id_squad_id_20b4127f_uniq UNIQUE (subject_id, squad_id);


--
-- Name: subjects_subject_students subjects_subject_students_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subject_students
    ADD CONSTRAINT subjects_subject_students_pkey PRIMARY KEY (id);


--
-- Name: subjects_subject_students subjects_subject_students_subject_id_profile_id_f0b01326_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subject_students
    ADD CONSTRAINT subjects_subject_students_subject_id_profile_id_f0b01326_uniq UNIQUE (subject_id, profile_id);


--
-- Name: subjects_subject_teacher subjects_subject_teacher_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subject_teacher
    ADD CONSTRAINT subjects_subject_teacher_pkey PRIMARY KEY (id);


--
-- Name: subjects_subject_teacher subjects_subject_teacher_subject_id_squad_id_01a946a1_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subject_teacher
    ADD CONSTRAINT subjects_subject_teacher_subject_id_squad_id_01a946a1_uniq UNIQUE (subject_id, profile_id);


--
-- Name: subjects_subjectmaterials_lessons subjects_subjectmaterial_subjectmaterials_id_less_2cf0f23c_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subjectmaterials_lessons
    ADD CONSTRAINT subjects_subjectmaterial_subjectmaterials_id_less_2cf0f23c_uniq UNIQUE (subjectmaterials_id, lesson_id);


--
-- Name: subjects_subjectmaterials_done_by subjects_subjectmaterial_subjectmaterials_id_prof_bd64afb8_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subjectmaterials_done_by
    ADD CONSTRAINT subjects_subjectmaterial_subjectmaterials_id_prof_bd64afb8_uniq UNIQUE (subjectmaterials_id, profile_id);


--
-- Name: subjects_subjectmaterials_done_by subjects_subjectmaterials_done_by_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subjectmaterials_done_by
    ADD CONSTRAINT subjects_subjectmaterials_done_by_pkey PRIMARY KEY (id);


--
-- Name: subjects_subjectmaterials_lessons subjects_subjectmaterials_lessons_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subjectmaterials_lessons
    ADD CONSTRAINT subjects_subjectmaterials_lessons_pkey PRIMARY KEY (id);


--
-- Name: subjects_subjectmaterials subjects_subjectmaterials_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subjectmaterials
    ADD CONSTRAINT subjects_subjectmaterials_pkey PRIMARY KEY (id);


--
-- Name: subjects_timeperiod subjects_timeperiod_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_timeperiod
    ADD CONSTRAINT subjects_timeperiod_pkey PRIMARY KEY (id);


--
-- Name: subjects_timeperiod_people subjects_timeperiod_stud_timeperiod_id_profile_id_6b541be7_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_timeperiod_people
    ADD CONSTRAINT subjects_timeperiod_stud_timeperiod_id_profile_id_6b541be7_uniq UNIQUE (timeperiod_id, profile_id);


--
-- Name: subjects_timeperiod_people subjects_timeperiod_students_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_timeperiod_people
    ADD CONSTRAINT subjects_timeperiod_students_pkey PRIMARY KEY (id);


--
-- Name: tasks_problemtag tasks_problemtag_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks_problemtag
    ADD CONSTRAINT tasks_problemtag_pkey PRIMARY KEY (id);


--
-- Name: tasks_solver tasks_solver_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks_solver
    ADD CONSTRAINT tasks_solver_pkey PRIMARY KEY (id);


--
-- Name: tasks_task tasks_task_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks_task
    ADD CONSTRAINT tasks_task_pkey PRIMARY KEY (id);


--
-- Name: tasks_task_tags tasks_task_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks_task_tags
    ADD CONSTRAINT tasks_task_tags_pkey PRIMARY KEY (id);


--
-- Name: tasks_task_tags tasks_task_tags_task_id_problemtag_id_eab2760d_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks_task_tags
    ADD CONSTRAINT tasks_task_tags_task_id_problemtag_id_eab2760d_uniq UNIQUE (task_id, problemtag_id);


--
-- Name: todolist_board todolist_board_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_board
    ADD CONSTRAINT todolist_board_pkey PRIMARY KEY (id);


--
-- Name: todolist_card_doc_list todolist_card_doc_list_card_id_document_id_260ffb28_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_card_doc_list
    ADD CONSTRAINT todolist_card_doc_list_card_id_document_id_260ffb28_uniq UNIQUE (card_id, document_id);


--
-- Name: todolist_card_doc_list todolist_card_doc_list_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_card_doc_list
    ADD CONSTRAINT todolist_card_doc_list_pkey PRIMARY KEY (id);


--
-- Name: todolist_card_metka_list todolist_card_metka_list_card_id_metka_id_1b9305eb_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_card_metka_list
    ADD CONSTRAINT todolist_card_metka_list_card_id_metka_id_1b9305eb_uniq UNIQUE (card_id, metka_id);


--
-- Name: todolist_card_metka_list todolist_card_metka_list_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_card_metka_list
    ADD CONSTRAINT todolist_card_metka_list_pkey PRIMARY KEY (id);


--
-- Name: todolist_card todolist_card_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_card
    ADD CONSTRAINT todolist_card_pkey PRIMARY KEY (id);


--
-- Name: todolist_card_user_list todolist_card_user_list_card_id_profile_id_6ca21cc2_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_card_user_list
    ADD CONSTRAINT todolist_card_user_list_card_id_profile_id_6ca21cc2_uniq UNIQUE (card_id, profile_id);


--
-- Name: todolist_card_user_list todolist_card_user_list_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_card_user_list
    ADD CONSTRAINT todolist_card_user_list_pkey PRIMARY KEY (id);


--
-- Name: todolist_column todolist_column_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_column
    ADD CONSTRAINT todolist_column_pkey PRIMARY KEY (id);


--
-- Name: todolist_comment_ffile todolist_comment_ffile_comment_id_document_id_6007815f_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_comment_ffile
    ADD CONSTRAINT todolist_comment_ffile_comment_id_document_id_6007815f_uniq UNIQUE (comment_id, document_id);


--
-- Name: todolist_comment_ffile todolist_comment_ffile_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_comment_ffile
    ADD CONSTRAINT todolist_comment_ffile_pkey PRIMARY KEY (id);


--
-- Name: todolist_comment todolist_comment_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_comment
    ADD CONSTRAINT todolist_comment_pkey PRIMARY KEY (id);


--
-- Name: todolist_document todolist_document_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_document
    ADD CONSTRAINT todolist_document_pkey PRIMARY KEY (id);


--
-- Name: todolist_metka todolist_metka_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_metka
    ADD CONSTRAINT todolist_metka_pkey PRIMARY KEY (id);


--
-- Name: accounts_corruption_author_profile_id_a61a18a3; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX accounts_corruption_author_profile_id_a61a18a3 ON public.accounts_corruption USING btree (author_profile_id);


--
-- Name: accounts_corruption_school_id_3f007975; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX accounts_corruption_school_id_3f007975 ON public.accounts_corruption USING btree (school_id);


--
-- Name: accounts_crmcard_author_profile_id_b53e9c89; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX accounts_crmcard_author_profile_id_b53e9c89 ON public.accounts_crmcard USING btree (author_profile_id);


--
-- Name: accounts_crmcard_column_id_10f5f8c7; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX accounts_crmcard_column_id_10f5f8c7 ON public.accounts_crmcard USING btree (column_id);


--
-- Name: accounts_crmcard_school_id_78d244c7; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX accounts_crmcard_school_id_78d244c7 ON public.accounts_crmcard USING btree (school_id);


--
-- Name: accounts_crmcolumn_school_id_ea52e7bf; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX accounts_crmcolumn_school_id_ea52e7bf ON public.accounts_crmcolumn USING btree (school_id);


--
-- Name: accounts_jobcategory_profession_id_0baad4b6; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX accounts_jobcategory_profession_id_0baad4b6 ON public.accounts_jobcategory USING btree (profession_id);


--
-- Name: accounts_profile_crm_age_id_5d6f09dd; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX accounts_profile_crm_age_id_5d6f09dd ON public.accounts_profile USING btree (crm_age_id);


--
-- Name: accounts_profile_crm_office_id_9ee96c12; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX accounts_profile_crm_office_id_9ee96c12 ON public.accounts_profile USING btree (crm_office_id);


--
-- Name: accounts_profile_crm_subject_id_15bf97b9; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX accounts_profile_crm_subject_id_15bf97b9 ON public.accounts_profile USING btree (crm_subject_id);


--
-- Name: accounts_profile_job_categories_jobcategory_id_940d3313; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX accounts_profile_job_categories_jobcategory_id_940d3313 ON public.accounts_profile_job_categories USING btree (jobcategory_id);


--
-- Name: accounts_profile_job_categories_profile_id_176685f0; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX accounts_profile_job_categories_profile_id_176685f0 ON public.accounts_profile_job_categories USING btree (profile_id);


--
-- Name: accounts_profile_profession_profession_id_6644c1ab; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX accounts_profile_profession_profession_id_6644c1ab ON public.accounts_profile_profession USING btree (profession_id);


--
-- Name: accounts_profile_profession_profile_id_cf10eb06; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX accounts_profile_profession_profile_id_cf10eb06 ON public.accounts_profile_profession USING btree (profile_id);


--
-- Name: accounts_profile_schools_profile_id_580359b5; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX accounts_profile_schools_profile_id_580359b5 ON public.accounts_profile_schools USING btree (profile_id);


--
-- Name: accounts_profile_schools_school_id_452cf335; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX accounts_profile_schools_school_id_452cf335 ON public.accounts_profile_schools USING btree (school_id);


--
-- Name: accounts_zaiavka_school_id_99265652; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX accounts_zaiavka_school_id_99265652 ON public.accounts_zaiavka USING btree (school_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: docs_card_column_id_f6cd3e90; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX docs_card_column_id_f6cd3e90 ON public.docs_card USING btree (column_id);


--
-- Name: docs_card_doc_list_card_id_46040571; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX docs_card_doc_list_card_id_46040571 ON public.docs_card_doc_list USING btree (card_id);


--
-- Name: docs_card_doc_list_document_id_ebbf5c6b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX docs_card_doc_list_document_id_ebbf5c6b ON public.docs_card_doc_list USING btree (document_id);


--
-- Name: docs_card_metka_list_card_id_1e9b4526; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX docs_card_metka_list_card_id_1e9b4526 ON public.docs_card_metka_list USING btree (card_id);


--
-- Name: docs_card_metka_list_metka_id_b07b30c3; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX docs_card_metka_list_metka_id_b07b30c3 ON public.docs_card_metka_list USING btree (metka_id);


--
-- Name: docs_card_slug_99525456; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX docs_card_slug_99525456 ON public.docs_card USING btree (slug);


--
-- Name: docs_card_slug_99525456_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX docs_card_slug_99525456_like ON public.docs_card USING btree (slug varchar_pattern_ops);


--
-- Name: docs_card_user_list_card_id_073d1a0f; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX docs_card_user_list_card_id_073d1a0f ON public.docs_card_user_list USING btree (card_id);


--
-- Name: docs_card_user_list_profile_id_df7a8432; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX docs_card_user_list_profile_id_df7a8432 ON public.docs_card_user_list USING btree (profile_id);


--
-- Name: docs_column_board_id_da98ddbe; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX docs_column_board_id_da98ddbe ON public.docs_column USING btree (board_id);


--
-- Name: docs_comment_author_profile_id_e4b8f6bb; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX docs_comment_author_profile_id_e4b8f6bb ON public.docs_comment USING btree (author_profile_id);


--
-- Name: docs_comment_card_id_0d2ec314; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX docs_comment_card_id_0d2ec314 ON public.docs_comment USING btree (card_id);


--
-- Name: docs_comment_ffile_comment_id_7a0aa710; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX docs_comment_ffile_comment_id_7a0aa710 ON public.docs_comment_ffile USING btree (comment_id);


--
-- Name: docs_comment_ffile_document_id_8771213e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX docs_comment_ffile_document_id_8771213e ON public.docs_comment_ffile USING btree (document_id);


--
-- Name: documents_documentcache_author_profile_id_5d920869; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX documents_documentcache_author_profile_id_5d920869 ON public.documents_documentcache USING btree (author_profile_id);


--
-- Name: documents_documentfolder_author_profile_id_168dbf53; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX documents_documentfolder_author_profile_id_168dbf53 ON public.documents_documentfolder USING btree (author_profile_id);


--
-- Name: documents_documentfolder_c_from_documentfolder_id_53c45978; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX documents_documentfolder_c_from_documentfolder_id_53c45978 ON public.documents_documentfolder_children USING btree (from_documentfolder_id);


--
-- Name: documents_documentfolder_children_to_documentfolder_id_e710efe3; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX documents_documentfolder_children_to_documentfolder_id_e710efe3 ON public.documents_documentfolder_children USING btree (to_documentfolder_id);


--
-- Name: documents_documentfolder_files_document_id_d045491d; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX documents_documentfolder_files_document_id_d045491d ON public.documents_documentfolder_files USING btree (document_id);


--
-- Name: documents_documentfolder_files_documentfolder_id_0993a6ec; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX documents_documentfolder_files_documentfolder_id_0993a6ec ON public.documents_documentfolder_files USING btree (documentfolder_id);


--
-- Name: documents_documentfolder_parent_id_24780762; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX documents_documentfolder_parent_id_24780762 ON public.documents_documentfolder USING btree (parent_id);


--
-- Name: documents_documentfolder_school_id_d46e6d92; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX documents_documentfolder_school_id_d46e6d92 ON public.documents_documentfolder USING btree (school_id);


--
-- Name: library_cache_author_profile_id_f57582c5; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX library_cache_author_profile_id_f57582c5 ON public.library_cache USING btree (author_profile_id);


--
-- Name: library_folder_author_profile_id_984c37e7; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX library_folder_author_profile_id_984c37e7 ON public.library_folder USING btree (author_profile_id);


--
-- Name: library_folder_children_from_folder_id_632a6323; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX library_folder_children_from_folder_id_632a6323 ON public.library_folder_children USING btree (from_folder_id);


--
-- Name: library_folder_children_to_folder_id_368cf890; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX library_folder_children_to_folder_id_368cf890 ON public.library_folder_children USING btree (to_folder_id);


--
-- Name: library_folder_lesson_list_folder_id_b2df3687; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX library_folder_lesson_list_folder_id_b2df3687 ON public.library_folder_lesson_list USING btree (folder_id);


--
-- Name: library_folder_lesson_list_lesson_id_588c6b56; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX library_folder_lesson_list_lesson_id_588c6b56 ON public.library_folder_lesson_list USING btree (lesson_id);


--
-- Name: library_folder_parent_id_35d39534; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX library_folder_parent_id_35d39534 ON public.library_folder USING btree (parent_id);


--
-- Name: library_folder_school_id_915b8da1; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX library_folder_school_id_915b8da1 ON public.library_folder USING btree (school_id);


--
-- Name: news_post_author_profile_id_dd51e0da; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX news_post_author_profile_id_dd51e0da ON public.news_post USING btree (author_profile_id);


--
-- Name: news_post_school_id_9ea3ede6; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX news_post_school_id_9ea3ede6 ON public.news_post USING btree (school_id);


--
-- Name: papers_comment_author_profile_id_217bbf7b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_comment_author_profile_id_217bbf7b ON public.papers_comment USING btree (author_profile_id);


--
-- Name: papers_comment_dislikes_comment_id_c9789ba0; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_comment_dislikes_comment_id_c9789ba0 ON public.papers_comment_dislikes USING btree (comment_id);


--
-- Name: papers_comment_dislikes_profile_id_d0713df0; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_comment_dislikes_profile_id_d0713df0 ON public.papers_comment_dislikes USING btree (profile_id);


--
-- Name: papers_comment_lesson_id_63ef49a7; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_comment_lesson_id_63ef49a7 ON public.papers_comment USING btree (lesson_id);


--
-- Name: papers_comment_likes_comment_id_548766f5; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_comment_likes_comment_id_548766f5 ON public.papers_comment_likes USING btree (comment_id);


--
-- Name: papers_comment_likes_profile_id_9464a34c; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_comment_likes_profile_id_9464a34c ON public.papers_comment_likes USING btree (profile_id);


--
-- Name: papers_comment_parent_id_e9ac922e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_comment_parent_id_e9ac922e ON public.papers_comment USING btree (parent_id);


--
-- Name: papers_course_author_profile_id_26c54296; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_course_author_profile_id_26c54296 ON public.papers_course USING btree (author_profile_id);


--
-- Name: papers_course_done_by_course_id_1e3211d7; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_course_done_by_course_id_1e3211d7 ON public.papers_course_done_by USING btree (course_id);


--
-- Name: papers_course_done_by_profile_id_5bd1faa2; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_course_done_by_profile_id_5bd1faa2 ON public.papers_course_done_by USING btree (profile_id);


--
-- Name: papers_course_lesson_course_id_4a2e59cd; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_course_lesson_course_id_4a2e59cd ON public.papers_course_lessons USING btree (course_id);


--
-- Name: papers_course_lesson_lesson_id_9b5aa6bc; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_course_lesson_lesson_id_9b5aa6bc ON public.papers_course_lessons USING btree (lesson_id);


--
-- Name: papers_course_school_id_a5751aea; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_course_school_id_a5751aea ON public.papers_course USING btree (school_id);


--
-- Name: papers_course_students_course_id_e9d72f5b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_course_students_course_id_e9d72f5b ON public.papers_course_students USING btree (course_id);


--
-- Name: papers_course_students_profile_id_3580ef8f; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_course_students_profile_id_3580ef8f ON public.papers_course_students USING btree (profile_id);


--
-- Name: papers_lesson_author_profile_id_7ab13ded; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_lesson_author_profile_id_7ab13ded ON public.papers_lesson USING btree (author_profile_id);


--
-- Name: papers_lesson_done_by_lesson_id_bf375d15; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_lesson_done_by_lesson_id_bf375d15 ON public.papers_lesson_done_by USING btree (lesson_id);


--
-- Name: papers_lesson_done_by_profile_id_b8bacad2; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_lesson_done_by_profile_id_b8bacad2 ON public.papers_lesson_done_by USING btree (profile_id);


--
-- Name: papers_lesson_papers_lesson_id_8328de31; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_lesson_papers_lesson_id_8328de31 ON public.papers_lesson_papers USING btree (lesson_id);


--
-- Name: papers_lesson_papers_paper_id_42810bfd; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_lesson_papers_paper_id_42810bfd ON public.papers_lesson_papers USING btree (paper_id);


--
-- Name: papers_lesson_school_id_752b8443; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_lesson_school_id_752b8443 ON public.papers_lesson USING btree (school_id);


--
-- Name: papers_paper_author_profile_id_340f6404; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_paper_author_profile_id_340f6404 ON public.papers_paper USING btree (author_profile_id);


--
-- Name: papers_paper_done_by_paper_id_e95461a0; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_paper_done_by_paper_id_e95461a0 ON public.papers_paper_done_by USING btree (paper_id);


--
-- Name: papers_paper_done_by_profile_id_305c697c; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_paper_done_by_profile_id_305c697c ON public.papers_paper_done_by USING btree (profile_id);


--
-- Name: papers_paper_school_id_5bce821d; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_paper_school_id_5bce821d ON public.papers_paper USING btree (school_id);


--
-- Name: papers_paper_subthemes_paper_id_dc8c7c5b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_paper_subthemes_paper_id_dc8c7c5b ON public.papers_paper_subthemes USING btree (paper_id);


--
-- Name: papers_paper_subthemes_subtheme_id_32a02d2f; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_paper_subthemes_subtheme_id_32a02d2f ON public.papers_paper_subthemes USING btree (subtheme_id);


--
-- Name: papers_subtheme_task_list_subtheme_id_c740e453; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_subtheme_task_list_subtheme_id_c740e453 ON public.papers_subtheme_task_list USING btree (subtheme_id);


--
-- Name: papers_subtheme_task_list_task_id_98db36fd; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX papers_subtheme_task_list_task_id_98db36fd ON public.papers_subtheme_task_list USING btree (task_id);


--
-- Name: schools_cabinett_school_id_1009cf46; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX schools_cabinett_school_id_1009cf46 ON public.schools_cabinet USING btree (school_id);


--
-- Name: schools_office_school_id_24f67cef; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX schools_office_school_id_24f67cef ON public.schools_office USING btree (school_id);


--
-- Name: schools_subjectage_school_id_872e9e21; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX schools_subjectage_school_id_872e9e21 ON public.schools_subjectage USING btree (school_id);


--
-- Name: schools_subjectcategory_school_id_ec78057d; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX schools_subjectcategory_school_id_ec78057d ON public.schools_subjectcategory USING btree (school_id);


--
-- Name: squads_squad_curator_profile_id_0fb1890d; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX squads_squad_curator_profile_id_0fb1890d ON public.squads_squad_curator USING btree (profile_id);


--
-- Name: squads_squad_curator_squad_id_c8344741; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX squads_squad_curator_squad_id_c8344741 ON public.squads_squad_curator USING btree (squad_id);


--
-- Name: squads_squad_school_id_1f083685; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX squads_squad_school_id_1f083685 ON public.squads_squad USING btree (school_id);


--
-- Name: squads_squad_slug_3a9bb852_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX squads_squad_slug_3a9bb852_like ON public.squads_squad USING btree (slug varchar_pattern_ops);


--
-- Name: squads_squad_students_profile_id_9d453c4f; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX squads_squad_students_profile_id_9d453c4f ON public.squads_squad_students USING btree (profile_id);


--
-- Name: squads_squad_students_squad_id_211f5eab; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX squads_squad_students_squad_id_211f5eab ON public.squads_squad_students USING btree (squad_id);


--
-- Name: subjects_attendance_school_id_505b09cb; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_attendance_school_id_505b09cb ON public.subjects_attendance USING btree (school_id);


--
-- Name: subjects_attendance_squad_id_fb25382b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_attendance_squad_id_fb25382b ON public.subjects_attendance USING btree (squad_id);


--
-- Name: subjects_attendance_student_id_76bf0737; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_attendance_student_id_76bf0737 ON public.subjects_attendance USING btree (student_id);


--
-- Name: subjects_attendance_subject_id_f20bf08b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_attendance_subject_id_f20bf08b ON public.subjects_attendance USING btree (subject_id);


--
-- Name: subjects_attendance_subject_materials_id_387e99e4; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_attendance_subject_materials_id_387e99e4 ON public.subjects_attendance USING btree (subject_materials_id);


--
-- Name: subjects_attendance_teacher_id_6a7986b6; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_attendance_teacher_id_6a7986b6 ON public.subjects_attendance USING btree (teacher_id);


--
-- Name: subjects_cacheattendance_squad_id_07196ce1; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_cacheattendance_squad_id_07196ce1 ON public.subjects_cacheattendance USING btree (squad_id);


--
-- Name: subjects_cacheattendance_subject_id_4080f5c9; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_cacheattendance_subject_id_4080f5c9 ON public.subjects_cacheattendance USING btree (subject_id);


--
-- Name: subjects_cell_day_id_81a3f696; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_cell_day_id_81a3f696 ON public.subjects_cell USING btree (day_id);


--
-- Name: subjects_cell_school_id_47d81844; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_cell_school_id_47d81844 ON public.subjects_cell USING btree (school_id);


--
-- Name: subjects_cell_time_period_id_bbfce574; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_cell_time_period_id_bbfce574 ON public.subjects_cell USING btree (time_period_id);


--
-- Name: subjects_lecture_age_id_05e7c3bd; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_lecture_age_id_05e7c3bd ON public.subjects_lecture USING btree (age_id);


--
-- Name: subjects_lecture_cabinet_id_1fa962a6; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_lecture_cabinet_id_1fa962a6 ON public.subjects_lecture USING btree (cabinet_id);


--
-- Name: subjects_lecture_category_id_a3f5e462; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_lecture_category_id_a3f5e462 ON public.subjects_lecture USING btree (category_id);


--
-- Name: subjects_lecture_cell_id_4e65eed3; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_lecture_cell_id_4e65eed3 ON public.subjects_lecture USING btree (cell_id);


--
-- Name: subjects_lecture_day_id_b6cc6ae2; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_lecture_day_id_b6cc6ae2 ON public.subjects_lecture USING btree (day_id);


--
-- Name: subjects_lecture_office_id_e0c82f9d; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_lecture_office_id_e0c82f9d ON public.subjects_lecture USING btree (office_id);


--
-- Name: subjects_lecture_people_lecture_id_3e9ebf4a; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_lecture_people_lecture_id_3e9ebf4a ON public.subjects_lecture_people USING btree (lecture_id);


--
-- Name: subjects_lecture_people_profile_id_e69731b9; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_lecture_people_profile_id_e69731b9 ON public.subjects_lecture_people USING btree (profile_id);


--
-- Name: subjects_lecture_school_id_eeeff0f1; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_lecture_school_id_eeeff0f1 ON public.subjects_lecture USING btree (school_id);


--
-- Name: subjects_lecture_squad_id_5d04be25; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_lecture_squad_id_5d04be25 ON public.subjects_lecture USING btree (squad_id);


--
-- Name: subjects_lecture_subject_id_f57e1dee; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_lecture_subject_id_f57e1dee ON public.subjects_lecture USING btree (subject_id);


--
-- Name: subjects_subject_age_id_0dc1415f; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_subject_age_id_0dc1415f ON public.subjects_subject USING btree (age_id);


--
-- Name: subjects_subject_category_id_1a0c2ea9; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_subject_category_id_1a0c2ea9 ON public.subjects_subject USING btree (category_id);


--
-- Name: subjects_subject_office_id_64b9618e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_subject_office_id_64b9618e ON public.subjects_subject USING btree (office_id);


--
-- Name: subjects_subject_school_id_12ea9f72; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_subject_school_id_12ea9f72 ON public.subjects_subject USING btree (school_id);


--
-- Name: subjects_subject_slug_730ccc60_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_subject_slug_730ccc60_like ON public.subjects_subject USING btree (slug varchar_pattern_ops);


--
-- Name: subjects_subject_squads_squad_id_0bb88e65; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_subject_squads_squad_id_0bb88e65 ON public.subjects_subject_squads USING btree (squad_id);


--
-- Name: subjects_subject_squads_subject_id_05d5bcbe; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_subject_squads_subject_id_05d5bcbe ON public.subjects_subject_squads USING btree (subject_id);


--
-- Name: subjects_subject_students_profile_id_135e52bc; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_subject_students_profile_id_135e52bc ON public.subjects_subject_students USING btree (profile_id);


--
-- Name: subjects_subject_students_subject_id_ef39d96c; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_subject_students_subject_id_ef39d96c ON public.subjects_subject_students USING btree (subject_id);


--
-- Name: subjects_subject_teacher_squad_id_4237c9b0; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_subject_teacher_squad_id_4237c9b0 ON public.subjects_subject_teacher USING btree (profile_id);


--
-- Name: subjects_subject_teacher_subject_id_ab994401; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_subject_teacher_subject_id_ab994401 ON public.subjects_subject_teacher USING btree (subject_id);


--
-- Name: subjects_subjectmaterials_done_by_profile_id_e673f8e2; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_subjectmaterials_done_by_profile_id_e673f8e2 ON public.subjects_subjectmaterials_done_by USING btree (profile_id);


--
-- Name: subjects_subjectmaterials_done_by_subjectmaterials_id_b74193a3; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_subjectmaterials_done_by_subjectmaterials_id_b74193a3 ON public.subjects_subjectmaterials_done_by USING btree (subjectmaterials_id);


--
-- Name: subjects_subjectmaterials_lessons_lesson_id_3454dc5a; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_subjectmaterials_lessons_lesson_id_3454dc5a ON public.subjects_subjectmaterials_lessons USING btree (lesson_id);


--
-- Name: subjects_subjectmaterials_lessons_subjectmaterials_id_4beb9475; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_subjectmaterials_lessons_subjectmaterials_id_4beb9475 ON public.subjects_subjectmaterials_lessons USING btree (subjectmaterials_id);


--
-- Name: subjects_subjectmaterials_school_id_aeea6cc7; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_subjectmaterials_school_id_aeea6cc7 ON public.subjects_subjectmaterials USING btree (school_id);


--
-- Name: subjects_subjectmaterials_subject_id_41103f23; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_subjectmaterials_subject_id_41103f23 ON public.subjects_subjectmaterials USING btree (subject_id);


--
-- Name: subjects_timeperiod_school_id_35e98e29; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_timeperiod_school_id_35e98e29 ON public.subjects_timeperiod USING btree (school_id);


--
-- Name: subjects_timeperiod_students_profile_id_82bcb7c3; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_timeperiod_students_profile_id_82bcb7c3 ON public.subjects_timeperiod_people USING btree (profile_id);


--
-- Name: subjects_timeperiod_students_timeperiod_id_06314ed9; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX subjects_timeperiod_students_timeperiod_id_06314ed9 ON public.subjects_timeperiod_people USING btree (timeperiod_id);


--
-- Name: tasks_solver_author_profile_id_32e8219d; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX tasks_solver_author_profile_id_32e8219d ON public.tasks_solver USING btree (author_profile_id);


--
-- Name: tasks_solver_task_id_43ea03f7; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX tasks_solver_task_id_43ea03f7 ON public.tasks_solver USING btree (task_id);


--
-- Name: tasks_task_author_profile_id_3f7380a9; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX tasks_task_author_profile_id_3f7380a9 ON public.tasks_task USING btree (author_profile_id);


--
-- Name: tasks_task_parent_id_ee6a2001; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX tasks_task_parent_id_ee6a2001 ON public.tasks_task USING btree (parent_id);


--
-- Name: tasks_task_slug_e3abf117; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX tasks_task_slug_e3abf117 ON public.tasks_task USING btree (slug);


--
-- Name: tasks_task_slug_e3abf117_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX tasks_task_slug_e3abf117_like ON public.tasks_task USING btree (slug varchar_pattern_ops);


--
-- Name: tasks_task_tags_problemtag_id_9d9e6568; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX tasks_task_tags_problemtag_id_9d9e6568 ON public.tasks_task_tags USING btree (problemtag_id);


--
-- Name: tasks_task_tags_task_id_7f3deefe; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX tasks_task_tags_task_id_7f3deefe ON public.tasks_task_tags USING btree (task_id);


--
-- Name: todolist_board_school_id_b62cb854; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX todolist_board_school_id_b62cb854 ON public.todolist_board USING btree (school_id);


--
-- Name: todolist_card_column_id_86b98c8f; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX todolist_card_column_id_86b98c8f ON public.todolist_card USING btree (column_id);


--
-- Name: todolist_card_doc_list_card_id_97a6393e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX todolist_card_doc_list_card_id_97a6393e ON public.todolist_card_doc_list USING btree (card_id);


--
-- Name: todolist_card_doc_list_document_id_93c5177a; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX todolist_card_doc_list_document_id_93c5177a ON public.todolist_card_doc_list USING btree (document_id);


--
-- Name: todolist_card_metka_list_card_id_0154d36e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX todolist_card_metka_list_card_id_0154d36e ON public.todolist_card_metka_list USING btree (card_id);


--
-- Name: todolist_card_metka_list_metka_id_bc443f8c; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX todolist_card_metka_list_metka_id_bc443f8c ON public.todolist_card_metka_list USING btree (metka_id);


--
-- Name: todolist_card_slug_476f1ea3; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX todolist_card_slug_476f1ea3 ON public.todolist_card USING btree (slug);


--
-- Name: todolist_card_slug_476f1ea3_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX todolist_card_slug_476f1ea3_like ON public.todolist_card USING btree (slug varchar_pattern_ops);


--
-- Name: todolist_card_user_list_card_id_6e0bbffd; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX todolist_card_user_list_card_id_6e0bbffd ON public.todolist_card_user_list USING btree (card_id);


--
-- Name: todolist_card_user_list_profile_id_53e81b73; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX todolist_card_user_list_profile_id_53e81b73 ON public.todolist_card_user_list USING btree (profile_id);


--
-- Name: todolist_column_board_id_74475da5; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX todolist_column_board_id_74475da5 ON public.todolist_column USING btree (board_id);


--
-- Name: todolist_comment_author_profile_id_e7986c6e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX todolist_comment_author_profile_id_e7986c6e ON public.todolist_comment USING btree (author_profile_id);


--
-- Name: todolist_comment_card_id_8a873a60; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX todolist_comment_card_id_8a873a60 ON public.todolist_comment USING btree (card_id);


--
-- Name: todolist_comment_ffile_comment_id_aaa8be9d; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX todolist_comment_ffile_comment_id_aaa8be9d ON public.todolist_comment_ffile USING btree (comment_id);


--
-- Name: todolist_comment_ffile_document_id_7348f886; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX todolist_comment_ffile_document_id_7348f886 ON public.todolist_comment_ffile USING btree (document_id);


--
-- Name: todolist_document_school_id_836dcd47; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX todolist_document_school_id_836dcd47 ON public.todolist_document USING btree (school_id);


--
-- Name: accounts_corruption accounts_corruption_author_profile_id_a61a18a3_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_corruption
    ADD CONSTRAINT accounts_corruption_author_profile_id_a61a18a3_fk_accounts_ FOREIGN KEY (author_profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_corruption accounts_corruption_school_id_3f007975_fk_schools_school_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_corruption
    ADD CONSTRAINT accounts_corruption_school_id_3f007975_fk_schools_school_id FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_crmcard accounts_crmcard_author_profile_id_b53e9c89_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_crmcard
    ADD CONSTRAINT accounts_crmcard_author_profile_id_b53e9c89_fk_accounts_ FOREIGN KEY (author_profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_crmcard accounts_crmcard_column_id_10f5f8c7_fk_accounts_crmcolumn_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_crmcard
    ADD CONSTRAINT accounts_crmcard_column_id_10f5f8c7_fk_accounts_crmcolumn_id FOREIGN KEY (column_id) REFERENCES public.accounts_crmcolumn(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_crmcard accounts_crmcard_school_id_78d244c7_fk_schools_school_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_crmcard
    ADD CONSTRAINT accounts_crmcard_school_id_78d244c7_fk_schools_school_id FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_crmcolumn accounts_crmcolumn_school_id_ea52e7bf_fk_schools_school_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_crmcolumn
    ADD CONSTRAINT accounts_crmcolumn_school_id_ea52e7bf_fk_schools_school_id FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_jobcategory accounts_jobcategory_profession_id_0baad4b6_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_jobcategory
    ADD CONSTRAINT accounts_jobcategory_profession_id_0baad4b6_fk_accounts_ FOREIGN KEY (profession_id) REFERENCES public.accounts_profession(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_misslesson accounts_misslesson_profile_id_fca77b26_fk_accounts_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_misslesson
    ADD CONSTRAINT accounts_misslesson_profile_id_fca77b26_fk_accounts_profile_id FOREIGN KEY (profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_profile accounts_profile_crm_age_id_5d6f09dd_fk_schools_subjectage_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profile
    ADD CONSTRAINT accounts_profile_crm_age_id_5d6f09dd_fk_schools_subjectage_id FOREIGN KEY (crm_age_id) REFERENCES public.schools_subjectage(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_profile accounts_profile_crm_office_id_9ee96c12_fk_schools_office_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profile
    ADD CONSTRAINT accounts_profile_crm_office_id_9ee96c12_fk_schools_office_id FOREIGN KEY (crm_office_id) REFERENCES public.schools_office(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_profile accounts_profile_crm_subject_id_15bf97b9_fk_schools_s; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profile
    ADD CONSTRAINT accounts_profile_crm_subject_id_15bf97b9_fk_schools_s FOREIGN KEY (crm_subject_id) REFERENCES public.schools_subjectcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_profile_job_categories accounts_profile_job_jobcategory_id_940d3313_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profile_job_categories
    ADD CONSTRAINT accounts_profile_job_jobcategory_id_940d3313_fk_accounts_ FOREIGN KEY (jobcategory_id) REFERENCES public.accounts_jobcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_profile_job_categories accounts_profile_job_profile_id_176685f0_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profile_job_categories
    ADD CONSTRAINT accounts_profile_job_profile_id_176685f0_fk_accounts_ FOREIGN KEY (profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_profile_profession accounts_profile_pro_profession_id_6644c1ab_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profile_profession
    ADD CONSTRAINT accounts_profile_pro_profession_id_6644c1ab_fk_accounts_ FOREIGN KEY (profession_id) REFERENCES public.accounts_profession(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_profile_profession accounts_profile_pro_profile_id_cf10eb06_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profile_profession
    ADD CONSTRAINT accounts_profile_pro_profile_id_cf10eb06_fk_accounts_ FOREIGN KEY (profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_profile_schools accounts_profile_sch_profile_id_580359b5_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profile_schools
    ADD CONSTRAINT accounts_profile_sch_profile_id_580359b5_fk_accounts_ FOREIGN KEY (profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_profile_schools accounts_profile_sch_school_id_452cf335_fk_schools_s; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profile_schools
    ADD CONSTRAINT accounts_profile_sch_school_id_452cf335_fk_schools_s FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_profile accounts_profile_user_id_49a85d32_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_profile
    ADD CONSTRAINT accounts_profile_user_id_49a85d32_fk FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_zaiavka accounts_zaiavka_school_id_99265652_fk_schools_school_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.accounts_zaiavka
    ADD CONSTRAINT accounts_zaiavka_school_id_99265652_fk_schools_school_id FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: docs_card docs_card_column_id_f6cd3e90_fk_docs_column_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_card
    ADD CONSTRAINT docs_card_column_id_f6cd3e90_fk_docs_column_id FOREIGN KEY (column_id) REFERENCES public.docs_column(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: docs_card_doc_list docs_card_doc_list_card_id_46040571_fk_docs_card_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_card_doc_list
    ADD CONSTRAINT docs_card_doc_list_card_id_46040571_fk_docs_card_id FOREIGN KEY (card_id) REFERENCES public.docs_card(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: docs_card_doc_list docs_card_doc_list_document_id_ebbf5c6b_fk_docs_document_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_card_doc_list
    ADD CONSTRAINT docs_card_doc_list_document_id_ebbf5c6b_fk_docs_document_id FOREIGN KEY (document_id) REFERENCES public.docs_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: docs_card_metka_list docs_card_metka_list_card_id_1e9b4526_fk_docs_card_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_card_metka_list
    ADD CONSTRAINT docs_card_metka_list_card_id_1e9b4526_fk_docs_card_id FOREIGN KEY (card_id) REFERENCES public.docs_card(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: docs_card_metka_list docs_card_metka_list_metka_id_b07b30c3_fk_docs_metka_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_card_metka_list
    ADD CONSTRAINT docs_card_metka_list_metka_id_b07b30c3_fk_docs_metka_id FOREIGN KEY (metka_id) REFERENCES public.docs_metka(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: docs_card_user_list docs_card_user_list_card_id_073d1a0f_fk_docs_card_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_card_user_list
    ADD CONSTRAINT docs_card_user_list_card_id_073d1a0f_fk_docs_card_id FOREIGN KEY (card_id) REFERENCES public.docs_card(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: docs_column docs_column_board_id_da98ddbe_fk_docs_board_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_column
    ADD CONSTRAINT docs_column_board_id_da98ddbe_fk_docs_board_id FOREIGN KEY (board_id) REFERENCES public.docs_board(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: docs_comment docs_comment_card_id_0d2ec314_fk_docs_card_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_comment
    ADD CONSTRAINT docs_comment_card_id_0d2ec314_fk_docs_card_id FOREIGN KEY (card_id) REFERENCES public.docs_card(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: docs_comment_ffile docs_comment_ffile_comment_id_7a0aa710_fk_docs_comment_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_comment_ffile
    ADD CONSTRAINT docs_comment_ffile_comment_id_7a0aa710_fk_docs_comment_id FOREIGN KEY (comment_id) REFERENCES public.docs_comment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: docs_comment_ffile docs_comment_ffile_document_id_8771213e_fk_docs_document_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.docs_comment_ffile
    ADD CONSTRAINT docs_comment_ffile_document_id_8771213e_fk_docs_document_id FOREIGN KEY (document_id) REFERENCES public.docs_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: documents_documentcache documents_documentca_author_profile_id_5d920869_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.documents_documentcache
    ADD CONSTRAINT documents_documentca_author_profile_id_5d920869_fk_accounts_ FOREIGN KEY (author_profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: documents_documentfolder documents_documentfo_author_profile_id_168dbf53_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.documents_documentfolder
    ADD CONSTRAINT documents_documentfo_author_profile_id_168dbf53_fk_accounts_ FOREIGN KEY (author_profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: documents_documentfolder_files documents_documentfo_document_id_d045491d_fk_todolist_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.documents_documentfolder_files
    ADD CONSTRAINT documents_documentfo_document_id_d045491d_fk_todolist_ FOREIGN KEY (document_id) REFERENCES public.todolist_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: documents_documentfolder_files documents_documentfo_documentfolder_id_0993a6ec_fk_documents; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.documents_documentfolder_files
    ADD CONSTRAINT documents_documentfo_documentfolder_id_0993a6ec_fk_documents FOREIGN KEY (documentfolder_id) REFERENCES public.documents_documentfolder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: documents_documentfolder_children documents_documentfo_from_documentfolder__53c45978_fk_documents; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.documents_documentfolder_children
    ADD CONSTRAINT documents_documentfo_from_documentfolder__53c45978_fk_documents FOREIGN KEY (from_documentfolder_id) REFERENCES public.documents_documentfolder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: documents_documentfolder documents_documentfo_parent_id_24780762_fk_documents; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.documents_documentfolder
    ADD CONSTRAINT documents_documentfo_parent_id_24780762_fk_documents FOREIGN KEY (parent_id) REFERENCES public.documents_documentfolder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: documents_documentfolder documents_documentfo_school_id_d46e6d92_fk_schools_s; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.documents_documentfolder
    ADD CONSTRAINT documents_documentfo_school_id_d46e6d92_fk_schools_s FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: documents_documentfolder_children documents_documentfo_to_documentfolder_id_e710efe3_fk_documents; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.documents_documentfolder_children
    ADD CONSTRAINT documents_documentfo_to_documentfolder_id_e710efe3_fk_documents FOREIGN KEY (to_documentfolder_id) REFERENCES public.documents_documentfolder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: library_cache library_cache_author_profile_id_f57582c5_fk_accounts_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.library_cache
    ADD CONSTRAINT library_cache_author_profile_id_f57582c5_fk_accounts_profile_id FOREIGN KEY (author_profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: library_folder library_folder_author_profile_id_984c37e7_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.library_folder
    ADD CONSTRAINT library_folder_author_profile_id_984c37e7_fk_accounts_ FOREIGN KEY (author_profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: library_folder_children library_folder_child_from_folder_id_632a6323_fk_library_f; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.library_folder_children
    ADD CONSTRAINT library_folder_child_from_folder_id_632a6323_fk_library_f FOREIGN KEY (from_folder_id) REFERENCES public.library_folder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: library_folder_children library_folder_child_to_folder_id_368cf890_fk_library_f; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.library_folder_children
    ADD CONSTRAINT library_folder_child_to_folder_id_368cf890_fk_library_f FOREIGN KEY (to_folder_id) REFERENCES public.library_folder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: library_folder_lesson_list library_folder_lesso_folder_id_b2df3687_fk_library_f; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.library_folder_lesson_list
    ADD CONSTRAINT library_folder_lesso_folder_id_b2df3687_fk_library_f FOREIGN KEY (folder_id) REFERENCES public.library_folder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: library_folder_lesson_list library_folder_lesso_lesson_id_588c6b56_fk_papers_le; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.library_folder_lesson_list
    ADD CONSTRAINT library_folder_lesso_lesson_id_588c6b56_fk_papers_le FOREIGN KEY (lesson_id) REFERENCES public.papers_lesson(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: library_folder library_folder_parent_id_35d39534_fk_library_folder_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.library_folder
    ADD CONSTRAINT library_folder_parent_id_35d39534_fk_library_folder_id FOREIGN KEY (parent_id) REFERENCES public.library_folder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: library_folder library_folder_school_id_915b8da1_fk_schools_school_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.library_folder
    ADD CONSTRAINT library_folder_school_id_915b8da1_fk_schools_school_id FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: news_post news_post_author_profile_id_dd51e0da_fk_accounts_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.news_post
    ADD CONSTRAINT news_post_author_profile_id_dd51e0da_fk_accounts_profile_id FOREIGN KEY (author_profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: news_post news_post_school_id_9ea3ede6_fk_schools_school_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.news_post
    ADD CONSTRAINT news_post_school_id_9ea3ede6_fk_schools_school_id FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_comment papers_comment_author_profile_id_217bbf7b_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_comment
    ADD CONSTRAINT papers_comment_author_profile_id_217bbf7b_fk_accounts_ FOREIGN KEY (author_profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_comment_dislikes papers_comment_disli_comment_id_c9789ba0_fk_papers_co; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_comment_dislikes
    ADD CONSTRAINT papers_comment_disli_comment_id_c9789ba0_fk_papers_co FOREIGN KEY (comment_id) REFERENCES public.papers_comment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_comment_dislikes papers_comment_disli_profile_id_d0713df0_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_comment_dislikes
    ADD CONSTRAINT papers_comment_disli_profile_id_d0713df0_fk_accounts_ FOREIGN KEY (profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_comment papers_comment_lesson_id_63ef49a7_fk_papers_lesson_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_comment
    ADD CONSTRAINT papers_comment_lesson_id_63ef49a7_fk_papers_lesson_id FOREIGN KEY (lesson_id) REFERENCES public.papers_lesson(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_comment_likes papers_comment_likes_comment_id_548766f5_fk_papers_comment_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_comment_likes
    ADD CONSTRAINT papers_comment_likes_comment_id_548766f5_fk_papers_comment_id FOREIGN KEY (comment_id) REFERENCES public.papers_comment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_comment_likes papers_comment_likes_profile_id_9464a34c_fk_accounts_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_comment_likes
    ADD CONSTRAINT papers_comment_likes_profile_id_9464a34c_fk_accounts_profile_id FOREIGN KEY (profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_comment papers_comment_parent_id_e9ac922e_fk_papers_comment_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_comment
    ADD CONSTRAINT papers_comment_parent_id_e9ac922e_fk_papers_comment_id FOREIGN KEY (parent_id) REFERENCES public.papers_comment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_course papers_course_author_profile_id_26c54296_fk_accounts_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_course
    ADD CONSTRAINT papers_course_author_profile_id_26c54296_fk_accounts_profile_id FOREIGN KEY (author_profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_course_done_by papers_course_done_b_profile_id_5bd1faa2_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_course_done_by
    ADD CONSTRAINT papers_course_done_b_profile_id_5bd1faa2_fk_accounts_ FOREIGN KEY (profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_course_done_by papers_course_done_by_course_id_1e3211d7_fk_papers_course_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_course_done_by
    ADD CONSTRAINT papers_course_done_by_course_id_1e3211d7_fk_papers_course_id FOREIGN KEY (course_id) REFERENCES public.papers_course(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_course_lessons papers_course_lessons_course_id_92bd188d_fk_papers_course_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_course_lessons
    ADD CONSTRAINT papers_course_lessons_course_id_92bd188d_fk_papers_course_id FOREIGN KEY (course_id) REFERENCES public.papers_course(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_course_lessons papers_course_lessons_lesson_id_8b1b09e6_fk_papers_lesson_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_course_lessons
    ADD CONSTRAINT papers_course_lessons_lesson_id_8b1b09e6_fk_papers_lesson_id FOREIGN KEY (lesson_id) REFERENCES public.papers_lesson(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_course papers_course_school_id_a5751aea_fk_schools_school_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_course
    ADD CONSTRAINT papers_course_school_id_a5751aea_fk_schools_school_id FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_course_students papers_course_studen_profile_id_3580ef8f_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_course_students
    ADD CONSTRAINT papers_course_studen_profile_id_3580ef8f_fk_accounts_ FOREIGN KEY (profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_course_students papers_course_students_course_id_e9d72f5b_fk_papers_course_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_course_students
    ADD CONSTRAINT papers_course_students_course_id_e9d72f5b_fk_papers_course_id FOREIGN KEY (course_id) REFERENCES public.papers_course(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_lesson papers_lesson_author_profile_id_7ab13ded_fk_accounts_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_lesson
    ADD CONSTRAINT papers_lesson_author_profile_id_7ab13ded_fk_accounts_profile_id FOREIGN KEY (author_profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_lesson_done_by papers_lesson_done_b_profile_id_b8bacad2_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_lesson_done_by
    ADD CONSTRAINT papers_lesson_done_b_profile_id_b8bacad2_fk_accounts_ FOREIGN KEY (profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_lesson_done_by papers_lesson_done_by_lesson_id_bf375d15_fk_papers_lesson_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_lesson_done_by
    ADD CONSTRAINT papers_lesson_done_by_lesson_id_bf375d15_fk_papers_lesson_id FOREIGN KEY (lesson_id) REFERENCES public.papers_lesson(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_lesson_papers papers_lesson_papers_lesson_id_8328de31_fk_papers_lesson_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_lesson_papers
    ADD CONSTRAINT papers_lesson_papers_lesson_id_8328de31_fk_papers_lesson_id FOREIGN KEY (lesson_id) REFERENCES public.papers_lesson(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_lesson_papers papers_lesson_papers_paper_id_42810bfd_fk_papers_paper_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_lesson_papers
    ADD CONSTRAINT papers_lesson_papers_paper_id_42810bfd_fk_papers_paper_id FOREIGN KEY (paper_id) REFERENCES public.papers_paper(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_lesson papers_lesson_school_id_752b8443_fk_schools_school_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_lesson
    ADD CONSTRAINT papers_lesson_school_id_752b8443_fk_schools_school_id FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_paper papers_paper_author_profile_id_340f6404_fk_accounts_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_paper
    ADD CONSTRAINT papers_paper_author_profile_id_340f6404_fk_accounts_profile_id FOREIGN KEY (author_profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_paper_done_by papers_paper_done_by_paper_id_e95461a0_fk_papers_paper_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_paper_done_by
    ADD CONSTRAINT papers_paper_done_by_paper_id_e95461a0_fk_papers_paper_id FOREIGN KEY (paper_id) REFERENCES public.papers_paper(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_paper_done_by papers_paper_done_by_profile_id_305c697c_fk_accounts_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_paper_done_by
    ADD CONSTRAINT papers_paper_done_by_profile_id_305c697c_fk_accounts_profile_id FOREIGN KEY (profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_paper papers_paper_school_id_5bce821d_fk_schools_school_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_paper
    ADD CONSTRAINT papers_paper_school_id_5bce821d_fk_schools_school_id FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_paper_subthemes papers_paper_subthem_subtheme_id_32a02d2f_fk_papers_su; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_paper_subthemes
    ADD CONSTRAINT papers_paper_subthem_subtheme_id_32a02d2f_fk_papers_su FOREIGN KEY (subtheme_id) REFERENCES public.papers_subtheme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_paper_subthemes papers_paper_subthemes_paper_id_dc8c7c5b_fk_papers_paper_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_paper_subthemes
    ADD CONSTRAINT papers_paper_subthemes_paper_id_dc8c7c5b_fk_papers_paper_id FOREIGN KEY (paper_id) REFERENCES public.papers_paper(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_subtheme_task_list papers_subtheme_task_list_task_id_98db36fd_fk_tasks_task_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_subtheme_task_list
    ADD CONSTRAINT papers_subtheme_task_list_task_id_98db36fd_fk_tasks_task_id FOREIGN KEY (task_id) REFERENCES public.tasks_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: papers_subtheme_task_list papers_subtheme_task_subtheme_id_c740e453_fk_papers_su; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.papers_subtheme_task_list
    ADD CONSTRAINT papers_subtheme_task_subtheme_id_c740e453_fk_papers_su FOREIGN KEY (subtheme_id) REFERENCES public.papers_subtheme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: schools_cabinet schools_cabinet_school_id_4aa7e7ce_fk_schools_school_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schools_cabinet
    ADD CONSTRAINT schools_cabinet_school_id_4aa7e7ce_fk_schools_school_id FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: schools_office schools_office_school_id_24f67cef_fk_schools_school_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schools_office
    ADD CONSTRAINT schools_office_school_id_24f67cef_fk_schools_school_id FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: schools_subjectage schools_subjectage_school_id_872e9e21_fk_schools_school_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schools_subjectage
    ADD CONSTRAINT schools_subjectage_school_id_872e9e21_fk_schools_school_id FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: schools_subjectcategory schools_subjectcategory_school_id_ec78057d_fk_schools_school_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schools_subjectcategory
    ADD CONSTRAINT schools_subjectcategory_school_id_ec78057d_fk_schools_school_id FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: squads_squad_curator squads_squad_curator_profile_id_0fb1890d_fk_accounts_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.squads_squad_curator
    ADD CONSTRAINT squads_squad_curator_profile_id_0fb1890d_fk_accounts_profile_id FOREIGN KEY (profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: squads_squad_curator squads_squad_curator_squad_id_c8344741_fk_squads_squad_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.squads_squad_curator
    ADD CONSTRAINT squads_squad_curator_squad_id_c8344741_fk_squads_squad_id FOREIGN KEY (squad_id) REFERENCES public.squads_squad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: squads_squad squads_squad_school_id_1f083685_fk_schools_school_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.squads_squad
    ADD CONSTRAINT squads_squad_school_id_1f083685_fk_schools_school_id FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: squads_squad_students squads_squad_student_profile_id_9d453c4f_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.squads_squad_students
    ADD CONSTRAINT squads_squad_student_profile_id_9d453c4f_fk_accounts_ FOREIGN KEY (profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: squads_squad_students squads_squad_students_squad_id_211f5eab_fk_squads_squad_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.squads_squad_students
    ADD CONSTRAINT squads_squad_students_squad_id_211f5eab_fk_squads_squad_id FOREIGN KEY (squad_id) REFERENCES public.squads_squad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_attendance subjects_attendance_school_id_505b09cb_fk_schools_school_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_attendance
    ADD CONSTRAINT subjects_attendance_school_id_505b09cb_fk_schools_school_id FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_attendance subjects_attendance_squad_id_fb25382b_fk_squads_squad_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_attendance
    ADD CONSTRAINT subjects_attendance_squad_id_fb25382b_fk_squads_squad_id FOREIGN KEY (squad_id) REFERENCES public.squads_squad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_attendance subjects_attendance_student_id_76bf0737_fk_accounts_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_attendance
    ADD CONSTRAINT subjects_attendance_student_id_76bf0737_fk_accounts_profile_id FOREIGN KEY (student_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_attendance subjects_attendance_subject_id_f20bf08b_fk_subjects_subject_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_attendance
    ADD CONSTRAINT subjects_attendance_subject_id_f20bf08b_fk_subjects_subject_id FOREIGN KEY (subject_id) REFERENCES public.subjects_subject(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_attendance subjects_attendance_subject_materials_id_387e99e4_fk_subjects_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_attendance
    ADD CONSTRAINT subjects_attendance_subject_materials_id_387e99e4_fk_subjects_ FOREIGN KEY (subject_materials_id) REFERENCES public.subjects_subjectmaterials(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_attendance subjects_attendance_teacher_id_6a7986b6_fk_accounts_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_attendance
    ADD CONSTRAINT subjects_attendance_teacher_id_6a7986b6_fk_accounts_profile_id FOREIGN KEY (teacher_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_cacheattendance subjects_cacheattend_profile_id_b2403679_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_cacheattendance
    ADD CONSTRAINT subjects_cacheattend_profile_id_b2403679_fk_accounts_ FOREIGN KEY (profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_cacheattendance subjects_cacheattend_subject_id_4080f5c9_fk_subjects_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_cacheattendance
    ADD CONSTRAINT subjects_cacheattend_subject_id_4080f5c9_fk_subjects_ FOREIGN KEY (subject_id) REFERENCES public.subjects_subject(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_cacheattendance subjects_cacheattendance_squad_id_07196ce1_fk_squads_squad_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_cacheattendance
    ADD CONSTRAINT subjects_cacheattendance_squad_id_07196ce1_fk_squads_squad_id FOREIGN KEY (squad_id) REFERENCES public.squads_squad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_cell subjects_cell_day_id_81a3f696_fk_subjects_day_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_cell
    ADD CONSTRAINT subjects_cell_day_id_81a3f696_fk_subjects_day_id FOREIGN KEY (day_id) REFERENCES public.subjects_day(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_cell subjects_cell_school_id_47d81844_fk_schools_school_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_cell
    ADD CONSTRAINT subjects_cell_school_id_47d81844_fk_schools_school_id FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_cell subjects_cell_time_period_id_bbfce574_fk_subjects_timeperiod_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_cell
    ADD CONSTRAINT subjects_cell_time_period_id_bbfce574_fk_subjects_timeperiod_id FOREIGN KEY (time_period_id) REFERENCES public.subjects_timeperiod(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_lecture subjects_lecture_age_id_05e7c3bd_fk_schools_subjectage_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_lecture
    ADD CONSTRAINT subjects_lecture_age_id_05e7c3bd_fk_schools_subjectage_id FOREIGN KEY (age_id) REFERENCES public.schools_subjectage(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_lecture subjects_lecture_cabinet_id_1fa962a6_fk_schools_cabinet_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_lecture
    ADD CONSTRAINT subjects_lecture_cabinet_id_1fa962a6_fk_schools_cabinet_id FOREIGN KEY (cabinet_id) REFERENCES public.schools_cabinet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_lecture subjects_lecture_category_id_a3f5e462_fk_schools_s; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_lecture
    ADD CONSTRAINT subjects_lecture_category_id_a3f5e462_fk_schools_s FOREIGN KEY (category_id) REFERENCES public.schools_subjectcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_lecture subjects_lecture_cell_id_4e65eed3_fk_subjects_cell_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_lecture
    ADD CONSTRAINT subjects_lecture_cell_id_4e65eed3_fk_subjects_cell_id FOREIGN KEY (cell_id) REFERENCES public.subjects_cell(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_lecture subjects_lecture_day_id_b6cc6ae2_fk_subjects_day_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_lecture
    ADD CONSTRAINT subjects_lecture_day_id_b6cc6ae2_fk_subjects_day_id FOREIGN KEY (day_id) REFERENCES public.subjects_day(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_lecture subjects_lecture_office_id_e0c82f9d_fk_schools_office_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_lecture
    ADD CONSTRAINT subjects_lecture_office_id_e0c82f9d_fk_schools_office_id FOREIGN KEY (office_id) REFERENCES public.schools_office(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_lecture_people subjects_lecture_peo_lecture_id_3e9ebf4a_fk_subjects_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_lecture_people
    ADD CONSTRAINT subjects_lecture_peo_lecture_id_3e9ebf4a_fk_subjects_ FOREIGN KEY (lecture_id) REFERENCES public.subjects_lecture(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_lecture_people subjects_lecture_peo_profile_id_e69731b9_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_lecture_people
    ADD CONSTRAINT subjects_lecture_peo_profile_id_e69731b9_fk_accounts_ FOREIGN KEY (profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_lecture subjects_lecture_school_id_eeeff0f1_fk_schools_school_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_lecture
    ADD CONSTRAINT subjects_lecture_school_id_eeeff0f1_fk_schools_school_id FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_lecture subjects_lecture_squad_id_5d04be25_fk_squads_squad_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_lecture
    ADD CONSTRAINT subjects_lecture_squad_id_5d04be25_fk_squads_squad_id FOREIGN KEY (squad_id) REFERENCES public.squads_squad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_lecture subjects_lecture_subject_id_f57e1dee_fk_subjects_subject_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_lecture
    ADD CONSTRAINT subjects_lecture_subject_id_f57e1dee_fk_subjects_subject_id FOREIGN KEY (subject_id) REFERENCES public.subjects_subject(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_subject subjects_subject_age_id_0dc1415f_fk_schools_subjectage_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subject
    ADD CONSTRAINT subjects_subject_age_id_0dc1415f_fk_schools_subjectage_id FOREIGN KEY (age_id) REFERENCES public.schools_subjectage(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_subject subjects_subject_category_id_1a0c2ea9_fk_schools_s; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subject
    ADD CONSTRAINT subjects_subject_category_id_1a0c2ea9_fk_schools_s FOREIGN KEY (category_id) REFERENCES public.schools_subjectcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_subject subjects_subject_office_id_64b9618e_fk_schools_office_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subject
    ADD CONSTRAINT subjects_subject_office_id_64b9618e_fk_schools_office_id FOREIGN KEY (office_id) REFERENCES public.schools_office(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_subject subjects_subject_school_id_12ea9f72_fk_schools_school_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subject
    ADD CONSTRAINT subjects_subject_school_id_12ea9f72_fk_schools_school_id FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_subject_squads subjects_subject_squ_subject_id_05d5bcbe_fk_subjects_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subject_squads
    ADD CONSTRAINT subjects_subject_squ_subject_id_05d5bcbe_fk_subjects_ FOREIGN KEY (subject_id) REFERENCES public.subjects_subject(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_subject_squads subjects_subject_squads_squad_id_0bb88e65_fk_squads_squad_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subject_squads
    ADD CONSTRAINT subjects_subject_squads_squad_id_0bb88e65_fk_squads_squad_id FOREIGN KEY (squad_id) REFERENCES public.squads_squad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_subject_students subjects_subject_stu_profile_id_135e52bc_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subject_students
    ADD CONSTRAINT subjects_subject_stu_profile_id_135e52bc_fk_accounts_ FOREIGN KEY (profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_subject_students subjects_subject_stu_subject_id_ef39d96c_fk_subjects_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subject_students
    ADD CONSTRAINT subjects_subject_stu_subject_id_ef39d96c_fk_subjects_ FOREIGN KEY (subject_id) REFERENCES public.subjects_subject(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_subject_teacher subjects_subject_tea_profile_id_573d4475_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subject_teacher
    ADD CONSTRAINT subjects_subject_tea_profile_id_573d4475_fk_accounts_ FOREIGN KEY (profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_subject_teacher subjects_subject_tea_subject_id_ab994401_fk_subjects_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subject_teacher
    ADD CONSTRAINT subjects_subject_tea_subject_id_ab994401_fk_subjects_ FOREIGN KEY (subject_id) REFERENCES public.subjects_subject(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_subjectmaterials_lessons subjects_subjectmate_lesson_id_3454dc5a_fk_papers_le; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subjectmaterials_lessons
    ADD CONSTRAINT subjects_subjectmate_lesson_id_3454dc5a_fk_papers_le FOREIGN KEY (lesson_id) REFERENCES public.papers_lesson(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_subjectmaterials_done_by subjects_subjectmate_profile_id_e673f8e2_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subjectmaterials_done_by
    ADD CONSTRAINT subjects_subjectmate_profile_id_e673f8e2_fk_accounts_ FOREIGN KEY (profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_subjectmaterials subjects_subjectmate_school_id_aeea6cc7_fk_schools_s; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subjectmaterials
    ADD CONSTRAINT subjects_subjectmate_school_id_aeea6cc7_fk_schools_s FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_subjectmaterials subjects_subjectmate_subject_id_41103f23_fk_subjects_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subjectmaterials
    ADD CONSTRAINT subjects_subjectmate_subject_id_41103f23_fk_subjects_ FOREIGN KEY (subject_id) REFERENCES public.subjects_subject(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_subjectmaterials_lessons subjects_subjectmate_subjectmaterials_id_4beb9475_fk_subjects_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subjectmaterials_lessons
    ADD CONSTRAINT subjects_subjectmate_subjectmaterials_id_4beb9475_fk_subjects_ FOREIGN KEY (subjectmaterials_id) REFERENCES public.subjects_subjectmaterials(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_subjectmaterials_done_by subjects_subjectmate_subjectmaterials_id_b74193a3_fk_subjects_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_subjectmaterials_done_by
    ADD CONSTRAINT subjects_subjectmate_subjectmaterials_id_b74193a3_fk_subjects_ FOREIGN KEY (subjectmaterials_id) REFERENCES public.subjects_subjectmaterials(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_timeperiod_people subjects_timeperiod__profile_id_41d05b96_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_timeperiod_people
    ADD CONSTRAINT subjects_timeperiod__profile_id_41d05b96_fk_accounts_ FOREIGN KEY (profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_timeperiod_people subjects_timeperiod__timeperiod_id_03e43541_fk_subjects_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_timeperiod_people
    ADD CONSTRAINT subjects_timeperiod__timeperiod_id_03e43541_fk_subjects_ FOREIGN KEY (timeperiod_id) REFERENCES public.subjects_timeperiod(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_timeperiod subjects_timeperiod_school_id_35e98e29_fk_schools_school_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.subjects_timeperiod
    ADD CONSTRAINT subjects_timeperiod_school_id_35e98e29_fk_schools_school_id FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_solver tasks_solver_author_profile_id_32e8219d_fk_accounts_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks_solver
    ADD CONSTRAINT tasks_solver_author_profile_id_32e8219d_fk_accounts_profile_id FOREIGN KEY (author_profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_solver tasks_solver_task_id_43ea03f7_fk_tasks_task_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks_solver
    ADD CONSTRAINT tasks_solver_task_id_43ea03f7_fk_tasks_task_id FOREIGN KEY (task_id) REFERENCES public.tasks_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_task tasks_task_author_profile_id_3f7380a9_fk_accounts_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks_task
    ADD CONSTRAINT tasks_task_author_profile_id_3f7380a9_fk_accounts_profile_id FOREIGN KEY (author_profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_task tasks_task_parent_id_ee6a2001_fk_tasks_task_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks_task
    ADD CONSTRAINT tasks_task_parent_id_ee6a2001_fk_tasks_task_id FOREIGN KEY (parent_id) REFERENCES public.tasks_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_task_tags tasks_task_tags_problemtag_id_9d9e6568_fk_tasks_problemtag_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks_task_tags
    ADD CONSTRAINT tasks_task_tags_problemtag_id_9d9e6568_fk_tasks_problemtag_id FOREIGN KEY (problemtag_id) REFERENCES public.tasks_problemtag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_task_tags tasks_task_tags_task_id_7f3deefe_fk_tasks_task_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.tasks_task_tags
    ADD CONSTRAINT tasks_task_tags_task_id_7f3deefe_fk_tasks_task_id FOREIGN KEY (task_id) REFERENCES public.tasks_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: todolist_board todolist_board_school_id_b62cb854_fk_schools_school_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_board
    ADD CONSTRAINT todolist_board_school_id_b62cb854_fk_schools_school_id FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: todolist_card todolist_card_column_id_86b98c8f_fk_todolist_column_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_card
    ADD CONSTRAINT todolist_card_column_id_86b98c8f_fk_todolist_column_id FOREIGN KEY (column_id) REFERENCES public.todolist_column(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: todolist_card_doc_list todolist_card_doc_li_document_id_93c5177a_fk_todolist_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_card_doc_list
    ADD CONSTRAINT todolist_card_doc_li_document_id_93c5177a_fk_todolist_ FOREIGN KEY (document_id) REFERENCES public.todolist_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: todolist_card_doc_list todolist_card_doc_list_card_id_97a6393e_fk_todolist_card_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_card_doc_list
    ADD CONSTRAINT todolist_card_doc_list_card_id_97a6393e_fk_todolist_card_id FOREIGN KEY (card_id) REFERENCES public.todolist_card(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: todolist_card_metka_list todolist_card_metka_list_card_id_0154d36e_fk_todolist_card_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_card_metka_list
    ADD CONSTRAINT todolist_card_metka_list_card_id_0154d36e_fk_todolist_card_id FOREIGN KEY (card_id) REFERENCES public.todolist_card(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: todolist_card_metka_list todolist_card_metka_list_metka_id_bc443f8c_fk_todolist_metka_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_card_metka_list
    ADD CONSTRAINT todolist_card_metka_list_metka_id_bc443f8c_fk_todolist_metka_id FOREIGN KEY (metka_id) REFERENCES public.todolist_metka(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: todolist_card_user_list todolist_card_user_l_profile_id_53e81b73_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_card_user_list
    ADD CONSTRAINT todolist_card_user_l_profile_id_53e81b73_fk_accounts_ FOREIGN KEY (profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: todolist_card_user_list todolist_card_user_list_card_id_6e0bbffd_fk_todolist_card_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_card_user_list
    ADD CONSTRAINT todolist_card_user_list_card_id_6e0bbffd_fk_todolist_card_id FOREIGN KEY (card_id) REFERENCES public.todolist_card(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: todolist_column todolist_column_board_id_74475da5_fk_todolist_board_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_column
    ADD CONSTRAINT todolist_column_board_id_74475da5_fk_todolist_board_id FOREIGN KEY (board_id) REFERENCES public.todolist_board(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: todolist_comment todolist_comment_author_profile_id_e7986c6e_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_comment
    ADD CONSTRAINT todolist_comment_author_profile_id_e7986c6e_fk_accounts_ FOREIGN KEY (author_profile_id) REFERENCES public.accounts_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: todolist_comment todolist_comment_card_id_8a873a60_fk_todolist_card_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_comment
    ADD CONSTRAINT todolist_comment_card_id_8a873a60_fk_todolist_card_id FOREIGN KEY (card_id) REFERENCES public.todolist_card(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: todolist_comment_ffile todolist_comment_ffi_comment_id_aaa8be9d_fk_todolist_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_comment_ffile
    ADD CONSTRAINT todolist_comment_ffi_comment_id_aaa8be9d_fk_todolist_ FOREIGN KEY (comment_id) REFERENCES public.todolist_comment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: todolist_comment_ffile todolist_comment_ffi_document_id_7348f886_fk_todolist_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_comment_ffile
    ADD CONSTRAINT todolist_comment_ffi_document_id_7348f886_fk_todolist_ FOREIGN KEY (document_id) REFERENCES public.todolist_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: todolist_document todolist_document_school_id_836dcd47_fk_schools_school_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.todolist_document
    ADD CONSTRAINT todolist_document_school_id_836dcd47_fk_schools_school_id FOREIGN KEY (school_id) REFERENCES public.schools_school(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

