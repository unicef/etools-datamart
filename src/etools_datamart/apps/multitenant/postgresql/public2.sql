--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.9
-- Dumped by pg_dump version 10.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: account_emailaddress; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.account_emailaddress (
    id integer NOT NULL,
    email character varying(254) NOT NULL,
    verified boolean NOT NULL,
    "primary" boolean NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.account_emailaddress_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.account_emailaddress_id_seq OWNED BY public.account_emailaddress.id;


--
-- Name: account_emailconfirmation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.account_emailconfirmation (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    sent timestamp with time zone,
    key character varying(64) NOT NULL,
    email_address_id integer NOT NULL
);


--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.account_emailconfirmation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.account_emailconfirmation_id_seq OWNED BY public.account_emailconfirmation.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: -
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


--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: categories_category; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.categories_category (
    id integer NOT NULL,
    "order" integer NOT NULL,
    module character varying(10) NOT NULL,
    description text NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    CONSTRAINT categories_category_order_check CHECK (("order" >= 0))
);


--
-- Name: categories_category_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.categories_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: categories_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.categories_category_id_seq OWNED BY public.categories_category.id;


--
-- Name: celery_taskmeta; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.celery_taskmeta (
    id integer NOT NULL,
    task_id character varying(255) NOT NULL,
    status character varying(50) NOT NULL,
    result text,
    date_done timestamp with time zone NOT NULL,
    traceback text,
    hidden boolean NOT NULL,
    meta text
);


--
-- Name: celery_taskmeta_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.celery_taskmeta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: celery_taskmeta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.celery_taskmeta_id_seq OWNED BY public.celery_taskmeta.id;


--
-- Name: celery_tasksetmeta; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.celery_tasksetmeta (
    id integer NOT NULL,
    taskset_id character varying(255) NOT NULL,
    result text NOT NULL,
    date_done timestamp with time zone NOT NULL,
    hidden boolean NOT NULL
);


--
-- Name: celery_tasksetmeta_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.celery_tasksetmeta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: celery_tasksetmeta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.celery_tasksetmeta_id_seq OWNED BY public.celery_tasksetmeta.id;


--
-- Name: corsheaders_corsmodel; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.corsheaders_corsmodel (
    id integer NOT NULL,
    cors character varying(255) NOT NULL
);


--
-- Name: corsheaders_corsmodel_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.corsheaders_corsmodel_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: corsheaders_corsmodel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.corsheaders_corsmodel_id_seq OWNED BY public.corsheaders_corsmodel.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: -
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


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_celery_beat_crontabschedule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_celery_beat_crontabschedule (
    id integer NOT NULL,
    minute character varying(240) NOT NULL,
    hour character varying(96) NOT NULL,
    day_of_week character varying(64) NOT NULL,
    day_of_month character varying(124) NOT NULL,
    month_of_year character varying(64) NOT NULL
);


--
-- Name: django_celery_beat_crontabschedule_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.django_celery_beat_crontabschedule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_celery_beat_crontabschedule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.django_celery_beat_crontabschedule_id_seq OWNED BY public.django_celery_beat_crontabschedule.id;


--
-- Name: django_celery_beat_intervalschedule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_celery_beat_intervalschedule (
    id integer NOT NULL,
    every integer NOT NULL,
    period character varying(24) NOT NULL
);


--
-- Name: django_celery_beat_intervalschedule_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.django_celery_beat_intervalschedule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_celery_beat_intervalschedule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.django_celery_beat_intervalschedule_id_seq OWNED BY public.django_celery_beat_intervalschedule.id;


--
-- Name: django_celery_beat_periodictask; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_celery_beat_periodictask (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    task character varying(200) NOT NULL,
    args text NOT NULL,
    kwargs text NOT NULL,
    queue character varying(200),
    exchange character varying(200),
    routing_key character varying(200),
    expires timestamp with time zone,
    enabled boolean NOT NULL,
    last_run_at timestamp with time zone,
    total_run_count integer NOT NULL,
    date_changed timestamp with time zone NOT NULL,
    description text NOT NULL,
    crontab_id integer,
    interval_id integer,
    solar_id integer,
    CONSTRAINT django_celery_beat_periodictask_total_run_count_check CHECK ((total_run_count >= 0))
);


--
-- Name: django_celery_beat_periodictask_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.django_celery_beat_periodictask_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_celery_beat_periodictask_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.django_celery_beat_periodictask_id_seq OWNED BY public.django_celery_beat_periodictask.id;


--
-- Name: django_celery_beat_periodictasks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_celery_beat_periodictasks (
    ident smallint NOT NULL,
    last_update timestamp with time zone NOT NULL
);


--
-- Name: django_celery_beat_solarschedule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_celery_beat_solarschedule (
    id integer NOT NULL,
    event character varying(24) NOT NULL,
    latitude numeric(9,6) NOT NULL,
    longitude numeric(9,6) NOT NULL
);


--
-- Name: django_celery_beat_solarschedule_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.django_celery_beat_solarschedule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_celery_beat_solarschedule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.django_celery_beat_solarschedule_id_seq OWNED BY public.django_celery_beat_solarschedule.id;


--
-- Name: django_celery_results_taskresult; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_celery_results_taskresult (
    id integer NOT NULL,
    task_id character varying(255) NOT NULL,
    status character varying(50) NOT NULL,
    content_type character varying(128) NOT NULL,
    content_encoding character varying(64) NOT NULL,
    result text,
    date_done timestamp with time zone NOT NULL,
    traceback text,
    hidden boolean NOT NULL,
    meta text
);


--
-- Name: django_celery_results_taskresult_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.django_celery_results_taskresult_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_celery_results_taskresult_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.django_celery_results_taskresult_id_seq OWNED BY public.django_celery_results_taskresult.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- Name: django_site; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.django_site_id_seq OWNED BY public.django_site.id;


--
-- Name: djcelery_crontabschedule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.djcelery_crontabschedule (
    id integer NOT NULL,
    minute character varying(64) NOT NULL,
    hour character varying(64) NOT NULL,
    day_of_week character varying(64) NOT NULL,
    day_of_month character varying(64) NOT NULL,
    month_of_year character varying(64) NOT NULL
);


--
-- Name: djcelery_crontabschedule_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.djcelery_crontabschedule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: djcelery_crontabschedule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.djcelery_crontabschedule_id_seq OWNED BY public.djcelery_crontabschedule.id;


--
-- Name: djcelery_intervalschedule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.djcelery_intervalschedule (
    id integer NOT NULL,
    every integer NOT NULL,
    period character varying(24) NOT NULL
);


--
-- Name: djcelery_intervalschedule_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.djcelery_intervalschedule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: djcelery_intervalschedule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.djcelery_intervalschedule_id_seq OWNED BY public.djcelery_intervalschedule.id;


--
-- Name: djcelery_periodictask; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.djcelery_periodictask (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    task character varying(200) NOT NULL,
    interval_id integer,
    crontab_id integer,
    args text NOT NULL,
    kwargs text NOT NULL,
    queue character varying(200),
    exchange character varying(200),
    routing_key character varying(200),
    expires timestamp with time zone,
    enabled boolean NOT NULL,
    last_run_at timestamp with time zone,
    total_run_count integer NOT NULL,
    date_changed timestamp with time zone NOT NULL,
    description text NOT NULL,
    CONSTRAINT djcelery_periodictask_total_run_count_check CHECK ((total_run_count >= 0))
);


--
-- Name: djcelery_periodictask_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.djcelery_periodictask_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: djcelery_periodictask_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.djcelery_periodictask_id_seq OWNED BY public.djcelery_periodictask.id;


--
-- Name: djcelery_periodictasks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.djcelery_periodictasks (
    ident smallint NOT NULL,
    last_update timestamp with time zone NOT NULL
);


--
-- Name: djcelery_taskstate; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.djcelery_taskstate (
    id integer NOT NULL,
    state character varying(64) NOT NULL,
    task_id character varying(36) NOT NULL,
    name character varying(200),
    tstamp timestamp with time zone NOT NULL,
    args text,
    kwargs text,
    eta timestamp with time zone,
    expires timestamp with time zone,
    result text,
    traceback text,
    runtime double precision,
    retries integer NOT NULL,
    worker_id integer,
    hidden boolean NOT NULL
);


--
-- Name: djcelery_taskstate_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.djcelery_taskstate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: djcelery_taskstate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.djcelery_taskstate_id_seq OWNED BY public.djcelery_taskstate.id;


--
-- Name: djcelery_workerstate; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.djcelery_workerstate (
    id integer NOT NULL,
    hostname character varying(255) NOT NULL,
    last_heartbeat timestamp with time zone
);


--
-- Name: djcelery_workerstate_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.djcelery_workerstate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: djcelery_workerstate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.djcelery_workerstate_id_seq OWNED BY public.djcelery_workerstate.id;


--
-- Name: drfpasswordless_callbacktoken; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.drfpasswordless_callbacktoken (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    to_alias character varying(40) NOT NULL,
    to_alias_type character varying(20) NOT NULL,
    key character varying(6) NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: easy_thumbnails_source; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.easy_thumbnails_source (
    id integer NOT NULL,
    storage_hash character varying(40) NOT NULL,
    name character varying(255) NOT NULL,
    modified timestamp with time zone NOT NULL
);


--
-- Name: easy_thumbnails_source_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.easy_thumbnails_source_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: easy_thumbnails_source_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.easy_thumbnails_source_id_seq OWNED BY public.easy_thumbnails_source.id;


--
-- Name: easy_thumbnails_thumbnail; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.easy_thumbnails_thumbnail (
    id integer NOT NULL,
    storage_hash character varying(40) NOT NULL,
    name character varying(255) NOT NULL,
    modified timestamp with time zone NOT NULL,
    source_id integer NOT NULL
);


--
-- Name: easy_thumbnails_thumbnail_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.easy_thumbnails_thumbnail_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: easy_thumbnails_thumbnail_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.easy_thumbnails_thumbnail_id_seq OWNED BY public.easy_thumbnails_thumbnail.id;


--
-- Name: easy_thumbnails_thumbnaildimensions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.easy_thumbnails_thumbnaildimensions (
    id integer NOT NULL,
    thumbnail_id integer NOT NULL,
    width integer,
    height integer,
    CONSTRAINT easy_thumbnails_thumbnaildimensions_height_check CHECK ((height >= 0)),
    CONSTRAINT easy_thumbnails_thumbnaildimensions_width_check CHECK ((width >= 0))
);


--
-- Name: easy_thumbnails_thumbnaildimensions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.easy_thumbnails_thumbnaildimensions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: easy_thumbnails_thumbnaildimensions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.easy_thumbnails_thumbnaildimensions_id_seq OWNED BY public.easy_thumbnails_thumbnaildimensions.id;


--
-- Name: environment_issuecheckconfig; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.environment_issuecheckconfig (
    id integer NOT NULL,
    check_id character varying(100) NOT NULL,
    is_active boolean NOT NULL
);


--
-- Name: environment_issuecheckconfig_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.environment_issuecheckconfig_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: environment_issuecheckconfig_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.environment_issuecheckconfig_id_seq OWNED BY public.environment_issuecheckconfig.id;


--
-- Name: environment_tenantflag; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.environment_tenantflag (
    id integer NOT NULL,
    authenticated boolean NOT NULL,
    created timestamp with time zone NOT NULL,
    everyone boolean,
    languages text NOT NULL,
    modified timestamp with time zone NOT NULL,
    name character varying(100) NOT NULL,
    note text NOT NULL,
    percent numeric(3,1),
    rollout boolean NOT NULL,
    staff boolean NOT NULL,
    superusers boolean NOT NULL,
    testing boolean NOT NULL
);


--
-- Name: environment_tenantflag_countries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.environment_tenantflag_countries (
    id integer NOT NULL,
    tenantflag_id integer NOT NULL,
    country_id integer NOT NULL
);


--
-- Name: environment_tenantflag_countries_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.environment_tenantflag_countries_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: environment_tenantflag_countries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.environment_tenantflag_countries_id_seq OWNED BY public.environment_tenantflag_countries.id;


--
-- Name: environment_tenantflag_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.environment_tenantflag_groups (
    id integer NOT NULL,
    tenantflag_id integer NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: environment_tenantflag_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.environment_tenantflag_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: environment_tenantflag_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.environment_tenantflag_groups_id_seq OWNED BY public.environment_tenantflag_groups.id;


--
-- Name: environment_tenantflag_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.environment_tenantflag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: environment_tenantflag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.environment_tenantflag_id_seq OWNED BY public.environment_tenantflag.id;


--
-- Name: environment_tenantflag_users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.environment_tenantflag_users (
    id integer NOT NULL,
    tenantflag_id integer NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: environment_tenantflag_users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.environment_tenantflag_users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: environment_tenantflag_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.environment_tenantflag_users_id_seq OWNED BY public.environment_tenantflag_users.id;


--
-- Name: environment_tenantswitch; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.environment_tenantswitch (
    id integer NOT NULL,
    active boolean NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    name character varying(100) NOT NULL,
    note text NOT NULL
);


--
-- Name: environment_tenantswitch_countries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.environment_tenantswitch_countries (
    id integer NOT NULL,
    tenantswitch_id integer NOT NULL,
    country_id integer NOT NULL
);


--
-- Name: environment_tenantswitch_countries_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.environment_tenantswitch_countries_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: environment_tenantswitch_countries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.environment_tenantswitch_countries_id_seq OWNED BY public.environment_tenantswitch_countries.id;


--
-- Name: environment_tenantswitch_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.environment_tenantswitch_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: environment_tenantswitch_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.environment_tenantswitch_id_seq OWNED BY public.environment_tenantswitch.id;


--
-- Name: filer_clipboard; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.filer_clipboard (
    id integer NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: filer_clipboard_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.filer_clipboard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: filer_clipboard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.filer_clipboard_id_seq OWNED BY public.filer_clipboard.id;


--
-- Name: filer_clipboarditem; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.filer_clipboarditem (
    id integer NOT NULL,
    clipboard_id integer NOT NULL,
    file_id integer NOT NULL
);


--
-- Name: filer_clipboarditem_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.filer_clipboarditem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: filer_clipboarditem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.filer_clipboarditem_id_seq OWNED BY public.filer_clipboarditem.id;


--
-- Name: filer_file; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.filer_file (
    id integer NOT NULL,
    file character varying(255),
    _file_size integer,
    sha1 character varying(40) NOT NULL,
    has_all_mandatory_data boolean NOT NULL,
    original_filename character varying(255),
    name character varying(255) NOT NULL,
    description text,
    uploaded_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    is_public boolean NOT NULL,
    folder_id integer,
    owner_id integer,
    polymorphic_ctype_id integer
);


--
-- Name: filer_file_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.filer_file_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: filer_file_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.filer_file_id_seq OWNED BY public.filer_file.id;


--
-- Name: filer_folder; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.filer_folder (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    uploaded_at timestamp with time zone NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    lft integer NOT NULL,
    rght integer NOT NULL,
    tree_id integer NOT NULL,
    level integer NOT NULL,
    owner_id integer,
    parent_id integer,
    CONSTRAINT filer_folder_level_check CHECK ((level >= 0)),
    CONSTRAINT filer_folder_lft_check CHECK ((lft >= 0)),
    CONSTRAINT filer_folder_rght_check CHECK ((rght >= 0)),
    CONSTRAINT filer_folder_tree_id_check CHECK ((tree_id >= 0))
);


--
-- Name: filer_folder_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.filer_folder_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: filer_folder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.filer_folder_id_seq OWNED BY public.filer_folder.id;


--
-- Name: filer_folderpermission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.filer_folderpermission (
    id integer NOT NULL,
    type smallint NOT NULL,
    everybody boolean NOT NULL,
    can_edit smallint,
    can_read smallint,
    can_add_children smallint,
    folder_id integer,
    group_id integer,
    user_id integer
);


--
-- Name: filer_folderpermission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.filer_folderpermission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: filer_folderpermission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.filer_folderpermission_id_seq OWNED BY public.filer_folderpermission.id;


--
-- Name: filer_image; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.filer_image (
    file_ptr_id integer NOT NULL,
    _height integer,
    _width integer,
    date_taken timestamp with time zone,
    default_alt_text character varying(255),
    default_caption character varying(255),
    author character varying(255),
    must_always_publish_author_credit boolean NOT NULL,
    must_always_publish_copyright boolean NOT NULL,
    subject_location character varying(64)
);


--
-- Name: generic_links_genericlink; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.generic_links_genericlink (
    id integer NOT NULL,
    content_type_id integer NOT NULL,
    object_id integer NOT NULL,
    url character varying(200) NOT NULL,
    title character varying(200) NOT NULL,
    description text,
    user_id integer,
    created_at timestamp with time zone NOT NULL,
    is_external boolean NOT NULL,
    CONSTRAINT generic_links_genericlink_object_id_check CHECK ((object_id >= 0))
);


--
-- Name: generic_links_genericlink_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.generic_links_genericlink_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: generic_links_genericlink_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.generic_links_genericlink_id_seq OWNED BY public.generic_links_genericlink.id;


--
-- Name: notification_notification; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notification_notification (
    id integer NOT NULL,
    type character varying(255) NOT NULL,
    object_id integer,
    recipients character varying(255)[] NOT NULL,
    sent_recipients character varying(255)[] NOT NULL,
    template_name character varying(255) NOT NULL,
    template_data jsonb,
    content_type_id integer,
    cc character varying(255)[] NOT NULL,
    from_address character varying(255),
    html_message text NOT NULL,
    sent_email_id integer,
    subject text NOT NULL,
    text_message text NOT NULL,
    CONSTRAINT notification_notification_object_id_check CHECK ((object_id >= 0))
);


--
-- Name: notification_notification_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.notification_notification_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: notification_notification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.notification_notification_id_seq OWNED BY public.notification_notification.id;


--
-- Name: permissions2_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.permissions2_permission (
    id integer NOT NULL,
    permission character varying(10) NOT NULL,
    permission_type character varying(10) NOT NULL,
    target character varying(100) NOT NULL,
    condition character varying(100)[] NOT NULL
);


--
-- Name: permissions2_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.permissions2_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: permissions2_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.permissions2_permission_id_seq OWNED BY public.permissions2_permission.id;


--
-- Name: post_office_attachment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.post_office_attachment (
    id integer NOT NULL,
    file character varying(100) NOT NULL,
    name character varying(255) NOT NULL,
    mimetype character varying(255) NOT NULL
);


--
-- Name: post_office_attachment_emails; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.post_office_attachment_emails (
    id integer NOT NULL,
    attachment_id integer NOT NULL,
    email_id integer NOT NULL
);


--
-- Name: post_office_attachment_emails_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.post_office_attachment_emails_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: post_office_attachment_emails_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.post_office_attachment_emails_id_seq OWNED BY public.post_office_attachment_emails.id;


--
-- Name: post_office_attachment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.post_office_attachment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: post_office_attachment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.post_office_attachment_id_seq OWNED BY public.post_office_attachment.id;


--
-- Name: post_office_email; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.post_office_email (
    id integer NOT NULL,
    from_email character varying(254) NOT NULL,
    "to" text NOT NULL,
    cc text NOT NULL,
    bcc text NOT NULL,
    subject character varying(989) NOT NULL,
    message text NOT NULL,
    html_message text NOT NULL,
    status smallint,
    priority smallint,
    created timestamp with time zone NOT NULL,
    last_updated timestamp with time zone NOT NULL,
    scheduled_time timestamp with time zone,
    headers text,
    context text,
    template_id integer,
    backend_alias character varying(64) NOT NULL,
    CONSTRAINT post_office_email_priority_check CHECK ((priority >= 0)),
    CONSTRAINT post_office_email_status_check CHECK ((status >= 0))
);


--
-- Name: post_office_email_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.post_office_email_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: post_office_email_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.post_office_email_id_seq OWNED BY public.post_office_email.id;


--
-- Name: post_office_emailtemplate; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.post_office_emailtemplate (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text NOT NULL,
    subject character varying(255) NOT NULL,
    content text NOT NULL,
    html_content text NOT NULL,
    created timestamp with time zone NOT NULL,
    last_updated timestamp with time zone NOT NULL,
    default_template_id integer,
    language character varying(12) NOT NULL
);


--
-- Name: post_office_emailtemplate_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.post_office_emailtemplate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: post_office_emailtemplate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.post_office_emailtemplate_id_seq OWNED BY public.post_office_emailtemplate.id;


--
-- Name: post_office_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.post_office_log (
    id integer NOT NULL,
    date timestamp with time zone NOT NULL,
    status smallint NOT NULL,
    exception_type character varying(255) NOT NULL,
    message text NOT NULL,
    email_id integer NOT NULL,
    CONSTRAINT post_office_log_status_check CHECK ((status >= 0))
);


--
-- Name: post_office_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.post_office_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: post_office_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.post_office_log_id_seq OWNED BY public.post_office_log.id;


--
-- Name: publics_airlinecompany; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.publics_airlinecompany (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    code integer NOT NULL,
    iata character varying(3) NOT NULL,
    icao character varying(3) NOT NULL,
    country character varying(255) NOT NULL,
    deleted_at timestamp with time zone NOT NULL
);


--
-- Name: publics_airlinecompany_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.publics_airlinecompany_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: publics_airlinecompany_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.publics_airlinecompany_id_seq OWNED BY public.publics_airlinecompany.id;


--
-- Name: publics_businessarea; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.publics_businessarea (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    code character varying(32) NOT NULL,
    region_id integer NOT NULL,
    default_currency_id integer,
    deleted_at timestamp with time zone NOT NULL
);


--
-- Name: publics_businessarea_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.publics_businessarea_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: publics_businessarea_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.publics_businessarea_id_seq OWNED BY public.publics_businessarea.id;


--
-- Name: publics_businessregion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.publics_businessregion (
    id integer NOT NULL,
    name character varying(16) NOT NULL,
    code character varying(2) NOT NULL,
    deleted_at timestamp with time zone NOT NULL
);


--
-- Name: publics_businessregion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.publics_businessregion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: publics_businessregion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.publics_businessregion_id_seq OWNED BY public.publics_businessregion.id;


--
-- Name: publics_country; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.publics_country (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    long_name character varying(128) NOT NULL,
    vision_code character varying(3),
    iso_2 character varying(2) NOT NULL,
    iso_3 character varying(3) NOT NULL,
    valid_from date,
    valid_to date,
    business_area_id integer,
    currency_id integer,
    deleted_at timestamp with time zone NOT NULL,
    dsa_code character varying(3) NOT NULL
);


--
-- Name: publics_country_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.publics_country_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: publics_country_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.publics_country_id_seq OWNED BY public.publics_country.id;


--
-- Name: publics_currency; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.publics_currency (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    code character varying(5) NOT NULL,
    decimal_places integer NOT NULL,
    deleted_at timestamp with time zone NOT NULL,
    CONSTRAINT publics_currency_decimal_places_check CHECK ((decimal_places >= 0))
);


--
-- Name: publics_currency_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.publics_currency_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: publics_currency_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.publics_currency_id_seq OWNED BY public.publics_currency.id;


--
-- Name: publics_dsarate; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.publics_dsarate (
    id integer NOT NULL,
    effective_to_date date NOT NULL,
    dsa_amount_usd numeric(20,4) NOT NULL,
    dsa_amount_60plus_usd numeric(20,4) NOT NULL,
    dsa_amount_local numeric(20,4) NOT NULL,
    dsa_amount_60plus_local numeric(20,4) NOT NULL,
    room_rate numeric(20,4) NOT NULL,
    finalization_date date NOT NULL,
    effective_from_date date NOT NULL,
    region_id integer NOT NULL
);


--
-- Name: publics_dsarate_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.publics_dsarate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: publics_dsarate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.publics_dsarate_id_seq OWNED BY public.publics_dsarate.id;


--
-- Name: publics_dsarateupload; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.publics_dsarateupload (
    id integer NOT NULL,
    dsa_file character varying(100) NOT NULL,
    status character varying(64) NOT NULL,
    upload_date timestamp with time zone NOT NULL,
    errors jsonb
);


--
-- Name: publics_dsarateupload_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.publics_dsarateupload_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: publics_dsarateupload_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.publics_dsarateupload_id_seq OWNED BY public.publics_dsarateupload.id;


--
-- Name: publics_dsaregion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.publics_dsaregion (
    id integer NOT NULL,
    area_name character varying(120) NOT NULL,
    area_code character varying(3) NOT NULL,
    country_id integer NOT NULL,
    deleted_at timestamp with time zone NOT NULL,
    user_defined boolean NOT NULL
);


--
-- Name: publics_dsaregion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.publics_dsaregion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: publics_dsaregion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.publics_dsaregion_id_seq OWNED BY public.publics_dsaregion.id;


--
-- Name: publics_exchangerate; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.publics_exchangerate (
    id integer NOT NULL,
    valid_from date NOT NULL,
    valid_to date NOT NULL,
    x_rate numeric(10,5) NOT NULL,
    currency_id integer NOT NULL,
    deleted_at timestamp with time zone NOT NULL
);


--
-- Name: publics_exchangerate_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.publics_exchangerate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: publics_exchangerate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.publics_exchangerate_id_seq OWNED BY public.publics_exchangerate.id;


--
-- Name: publics_fund; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.publics_fund (
    id integer NOT NULL,
    name character varying(25) NOT NULL,
    deleted_at timestamp with time zone NOT NULL
);


--
-- Name: publics_fund_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.publics_fund_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: publics_fund_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.publics_fund_id_seq OWNED BY public.publics_fund.id;


--
-- Name: publics_grant; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.publics_grant (
    id integer NOT NULL,
    name character varying(25) NOT NULL,
    deleted_at timestamp with time zone NOT NULL
);


--
-- Name: publics_grant_funds; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.publics_grant_funds (
    id integer NOT NULL,
    grant_id integer NOT NULL,
    fund_id integer NOT NULL
);


--
-- Name: publics_grant_funds_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.publics_grant_funds_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: publics_grant_funds_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.publics_grant_funds_id_seq OWNED BY public.publics_grant_funds.id;


--
-- Name: publics_grant_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.publics_grant_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: publics_grant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.publics_grant_id_seq OWNED BY public.publics_grant.id;


--
-- Name: publics_travelagent; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.publics_travelagent (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    code character varying(128) NOT NULL,
    city character varying(128) NOT NULL,
    country_id integer NOT NULL,
    expense_type_id integer NOT NULL,
    deleted_at timestamp with time zone NOT NULL
);


--
-- Name: publics_travelagent_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.publics_travelagent_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: publics_travelagent_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.publics_travelagent_id_seq OWNED BY public.publics_travelagent.id;


--
-- Name: publics_travelexpensetype; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.publics_travelexpensetype (
    id integer NOT NULL,
    title character varying(128) NOT NULL,
    vendor_number character varying(128) NOT NULL,
    rank integer NOT NULL,
    deleted_at timestamp with time zone NOT NULL,
    CONSTRAINT publics_travelexpensetype_rank_check CHECK ((rank >= 0))
);


--
-- Name: publics_travelexpensetype_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.publics_travelexpensetype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: publics_travelexpensetype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.publics_travelexpensetype_id_seq OWNED BY public.publics_travelexpensetype.id;


--
-- Name: publics_wbs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.publics_wbs (
    id integer NOT NULL,
    name character varying(25) NOT NULL,
    business_area_id integer,
    deleted_at timestamp with time zone NOT NULL
);


--
-- Name: publics_wbs_grants; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.publics_wbs_grants (
    id integer NOT NULL,
    wbs_id integer NOT NULL,
    grant_id integer NOT NULL
);


--
-- Name: publics_wbs_grants_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.publics_wbs_grants_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: publics_wbs_grants_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.publics_wbs_grants_id_seq OWNED BY public.publics_wbs_grants.id;


--
-- Name: publics_wbs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.publics_wbs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: publics_wbs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.publics_wbs_id_seq OWNED BY public.publics_wbs.id;


--
-- Name: purchase_order_auditorfirm; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.purchase_order_auditorfirm (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    vendor_number character varying(30) NOT NULL,
    name character varying(255) NOT NULL,
    street_address character varying(500) NOT NULL,
    city character varying(255) NOT NULL,
    postal_code character varying(32) NOT NULL,
    country character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    phone_number character varying(32) NOT NULL,
    blocked boolean NOT NULL,
    hidden boolean NOT NULL,
    deleted_flag boolean NOT NULL,
    vision_synced boolean NOT NULL,
    unicef_users_allowed boolean NOT NULL
);


--
-- Name: purchase_order_auditorfirm_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.purchase_order_auditorfirm_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: purchase_order_auditorfirm_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.purchase_order_auditorfirm_id_seq OWNED BY public.purchase_order_auditorfirm.id;


--
-- Name: purchase_order_auditorstaffmember; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.purchase_order_auditorstaffmember (
    id integer NOT NULL,
    auditor_firm_id integer NOT NULL,
    user_id integer NOT NULL,
    hidden boolean NOT NULL
);


--
-- Name: purchase_order_auditorstaffmember_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.purchase_order_auditorstaffmember_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: purchase_order_auditorstaffmember_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.purchase_order_auditorstaffmember_id_seq OWNED BY public.purchase_order_auditorstaffmember.id;


--
-- Name: purchase_order_purchaseorder; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.purchase_order_purchaseorder (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    order_number character varying(30),
    contract_start_date date,
    contract_end_date date,
    auditor_firm_id integer NOT NULL
);


--
-- Name: purchase_order_purchaseorder_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.purchase_order_purchaseorder_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: purchase_order_purchaseorder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.purchase_order_purchaseorder_id_seq OWNED BY public.purchase_order_purchaseorder.id;


--
-- Name: purchase_order_purchaseorderitem; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.purchase_order_purchaseorderitem (
    id integer NOT NULL,
    number integer NOT NULL,
    purchase_order_id integer NOT NULL
);


--
-- Name: purchase_order_purchaseorderitem_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.purchase_order_purchaseorderitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: purchase_order_purchaseorderitem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.purchase_order_purchaseorderitem_id_seq OWNED BY public.purchase_order_purchaseorderitem.id;


--
-- Name: registration_emailregistrationprofile; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.registration_emailregistrationprofile (
    registrationprofile_ptr_id integer NOT NULL
);


--
-- Name: registration_registrationprofile; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.registration_registrationprofile (
    id integer NOT NULL,
    user_id integer NOT NULL,
    activation_key character varying(40) NOT NULL
);


--
-- Name: registration_registrationprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.registration_registrationprofile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: registration_registrationprofile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.registration_registrationprofile_id_seq OWNED BY public.registration_registrationprofile.id;


--
-- Name: reversion_revision; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.reversion_revision (
    id integer NOT NULL,
    manager_slug character varying(191) NOT NULL,
    date_created timestamp with time zone NOT NULL,
    user_id integer,
    comment text NOT NULL
);


--
-- Name: reversion_revision_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.reversion_revision_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reversion_revision_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.reversion_revision_id_seq OWNED BY public.reversion_revision.id;


--
-- Name: reversion_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.reversion_version (
    id integer NOT NULL,
    revision_id integer NOT NULL,
    object_id text NOT NULL,
    object_id_int integer,
    content_type_id integer NOT NULL,
    format character varying(255) NOT NULL,
    serialized_data text NOT NULL,
    object_repr text NOT NULL
);


--
-- Name: reversion_version_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.reversion_version_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reversion_version_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.reversion_version_id_seq OWNED BY public.reversion_version.id;


--
-- Name: socialaccount_socialaccount; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.socialaccount_socialaccount (
    id integer NOT NULL,
    provider character varying(30) NOT NULL,
    uid character varying(191) NOT NULL,
    last_login timestamp with time zone NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    extra_data text NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.socialaccount_socialaccount_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.socialaccount_socialaccount_id_seq OWNED BY public.socialaccount_socialaccount.id;


--
-- Name: socialaccount_socialapp; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.socialaccount_socialapp (
    id integer NOT NULL,
    provider character varying(30) NOT NULL,
    name character varying(40) NOT NULL,
    client_id character varying(191) NOT NULL,
    secret character varying(191) NOT NULL,
    key character varying(191) NOT NULL
);


--
-- Name: socialaccount_socialapp_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.socialaccount_socialapp_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: socialaccount_socialapp_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.socialaccount_socialapp_id_seq OWNED BY public.socialaccount_socialapp.id;


--
-- Name: socialaccount_socialapp_sites; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.socialaccount_socialapp_sites (
    id integer NOT NULL,
    socialapp_id integer NOT NULL,
    site_id integer NOT NULL
);


--
-- Name: socialaccount_socialapp_sites_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.socialaccount_socialapp_sites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: socialaccount_socialapp_sites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.socialaccount_socialapp_sites_id_seq OWNED BY public.socialaccount_socialapp_sites.id;


--
-- Name: socialaccount_socialtoken; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.socialaccount_socialtoken (
    id integer NOT NULL,
    token text NOT NULL,
    token_secret text NOT NULL,
    expires_at timestamp with time zone,
    account_id integer NOT NULL,
    app_id integer NOT NULL
);


--
-- Name: socialaccount_socialtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.socialaccount_socialtoken_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: socialaccount_socialtoken_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.socialaccount_socialtoken_id_seq OWNED BY public.socialaccount_socialtoken.id;


--
-- Name: tpmpartners_tpmpartner; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tpmpartners_tpmpartner (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    vendor_number character varying(30) NOT NULL,
    name character varying(255) NOT NULL,
    street_address character varying(500) NOT NULL,
    city character varying(255) NOT NULL,
    postal_code character varying(32) NOT NULL,
    country character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    phone_number character varying(32) NOT NULL,
    vision_synced boolean NOT NULL,
    blocked boolean NOT NULL,
    hidden boolean NOT NULL,
    deleted_flag boolean NOT NULL
);


--
-- Name: tpmpartners_tpmpartner_countries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tpmpartners_tpmpartner_countries (
    id integer NOT NULL,
    tpmpartner_id integer NOT NULL,
    country_id integer NOT NULL
);


--
-- Name: tpmpartners_tpmpartner_countries_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tpmpartners_tpmpartner_countries_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tpmpartners_tpmpartner_countries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tpmpartners_tpmpartner_countries_id_seq OWNED BY public.tpmpartners_tpmpartner_countries.id;


--
-- Name: tpmpartners_tpmpartner_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tpmpartners_tpmpartner_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tpmpartners_tpmpartner_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tpmpartners_tpmpartner_id_seq OWNED BY public.tpmpartners_tpmpartner.id;


--
-- Name: tpmpartners_tpmpartnerstaffmember; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tpmpartners_tpmpartnerstaffmember (
    id integer NOT NULL,
    receive_tpm_notifications boolean NOT NULL,
    tpm_partner_id integer NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: tpmpartners_tpmpartnerstaffmember_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tpmpartners_tpmpartnerstaffmember_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tpmpartners_tpmpartnerstaffmember_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tpmpartners_tpmpartnerstaffmember_id_seq OWNED BY public.tpmpartners_tpmpartnerstaffmember.id;


--
-- Name: unicef_notification_notification; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.unicef_notification_notification (
    id integer NOT NULL,
    method_type character varying(255) NOT NULL,
    object_id integer,
    from_address character varying(255),
    recipients character varying(255)[] NOT NULL,
    cc character varying(255)[] NOT NULL,
    sent_recipients character varying(255)[] NOT NULL,
    template_name character varying(255) NOT NULL,
    template_data jsonb,
    subject text NOT NULL,
    text_message text NOT NULL,
    html_message text NOT NULL,
    content_type_id integer,
    sent_email_id integer,
    CONSTRAINT unicef_notification_notification_object_id_check CHECK ((object_id >= 0))
);


--
-- Name: unicef_notification_notification_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.unicef_notification_notification_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: unicef_notification_notification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.unicef_notification_notification_id_seq OWNED BY public.unicef_notification_notification.id;


--
-- Name: users_country; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users_country (
    id integer NOT NULL,
    domain_url character varying(128) NOT NULL,
    schema_name character varying(63) NOT NULL,
    name character varying(100) NOT NULL,
    business_area_code character varying(10) NOT NULL,
    initial_zoom integer NOT NULL,
    latitude numeric(8,5),
    longitude numeric(8,5),
    country_short_code character varying(10) NOT NULL,
    vision_sync_enabled boolean NOT NULL,
    vision_last_synced timestamp with time zone,
    threshold_tae_usd numeric(20,4),
    threshold_tre_usd numeric(20,4),
    local_currency_id integer,
    long_name character varying(255) NOT NULL
);


--
-- Name: users_country_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_country_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_country_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_country_id_seq OWNED BY public.users_country.id;


--
-- Name: users_country_offices; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users_country_offices (
    id integer NOT NULL,
    country_id integer NOT NULL,
    office_id integer NOT NULL
);


--
-- Name: users_country_offices_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_country_offices_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_country_offices_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_country_offices_id_seq OWNED BY public.users_country_offices.id;


--
-- Name: users_equitrackregistrationmodel; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users_equitrackregistrationmodel (
    registrationprofile_ptr_id integer NOT NULL
);


--
-- Name: users_office; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users_office (
    id integer NOT NULL,
    name character varying(254) NOT NULL,
    zonal_chief_id integer
);


--
-- Name: users_office_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_office_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_office_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_office_id_seq OWNED BY public.users_office.id;


--
-- Name: users_section; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users_section (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    code character varying(32)
);


--
-- Name: users_section_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_section_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_section_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_section_id_seq OWNED BY public.users_section.id;


--
-- Name: users_userprofile; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users_userprofile (
    id integer NOT NULL,
    job_title character varying(255),
    phone_number character varying(255),
    country_id integer,
    office_id integer,
    user_id integer NOT NULL,
    country_override_id integer,
    partner_staff_member integer,
    guid character varying(40),
    org_unit_code character varying(32),
    org_unit_name character varying(64),
    post_number character varying(32),
    post_title character varying(64),
    staff_id character varying(32),
    vendor_number character varying(32),
    oic_id integer,
    supervisor_id integer
);


--
-- Name: users_userprofile_countries_available; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users_userprofile_countries_available (
    id integer NOT NULL,
    userprofile_id integer NOT NULL,
    country_id integer NOT NULL
);


--
-- Name: users_userprofile_countries_available_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_userprofile_countries_available_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_userprofile_countries_available_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_userprofile_countries_available_id_seq OWNED BY public.users_userprofile_countries_available.id;


--
-- Name: users_userprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_userprofile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_userprofile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_userprofile_id_seq OWNED BY public.users_userprofile.id;


--
-- Name: users_workspacecounter; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users_workspacecounter (
    id integer NOT NULL,
    travel_reference_number_counter integer NOT NULL,
    travel_invoice_reference_number_counter integer NOT NULL,
    workspace_id integer NOT NULL,
    CONSTRAINT users_workspacecounter_travel_invoice_reference_number_co_check CHECK ((travel_invoice_reference_number_counter >= 0)),
    CONSTRAINT users_workspacecounter_travel_reference_number_counter_check CHECK ((travel_reference_number_counter >= 0))
);


--
-- Name: users_workspacecounter_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_workspacecounter_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_workspacecounter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_workspacecounter_id_seq OWNED BY public.users_workspacecounter.id;


--
-- Name: vision_visionsynclog; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.vision_visionsynclog (
    id integer NOT NULL,
    handler_name character varying(50) NOT NULL,
    total_records integer NOT NULL,
    total_processed integer NOT NULL,
    successful boolean NOT NULL,
    exception_message text NOT NULL,
    date_processed timestamp with time zone NOT NULL,
    country_id integer NOT NULL,
    details character varying(2048) NOT NULL
);


--
-- Name: vision_visionsynclog_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.vision_visionsynclog_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: vision_visionsynclog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.vision_visionsynclog_id_seq OWNED BY public.vision_visionsynclog.id;


--
-- Name: waffle_flag; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.waffle_flag (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    everyone boolean,
    percent numeric(3,1),
    testing boolean NOT NULL,
    superusers boolean NOT NULL,
    staff boolean NOT NULL,
    authenticated boolean NOT NULL,
    languages text NOT NULL,
    rollout boolean NOT NULL,
    note text NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL
);


--
-- Name: waffle_flag_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.waffle_flag_groups (
    id integer NOT NULL,
    flag_id integer NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: waffle_flag_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.waffle_flag_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: waffle_flag_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.waffle_flag_groups_id_seq OWNED BY public.waffle_flag_groups.id;


--
-- Name: waffle_flag_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.waffle_flag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: waffle_flag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.waffle_flag_id_seq OWNED BY public.waffle_flag.id;


--
-- Name: waffle_flag_users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.waffle_flag_users (
    id integer NOT NULL,
    flag_id integer NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: waffle_flag_users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.waffle_flag_users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: waffle_flag_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.waffle_flag_users_id_seq OWNED BY public.waffle_flag_users.id;


--
-- Name: waffle_sample; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.waffle_sample (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    percent numeric(4,1) NOT NULL,
    note text NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL
);


--
-- Name: waffle_sample_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.waffle_sample_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: waffle_sample_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.waffle_sample_id_seq OWNED BY public.waffle_sample.id;


--
-- Name: waffle_switch; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.waffle_switch (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    active boolean NOT NULL,
    note text NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL
);


--
-- Name: waffle_switch_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.waffle_switch_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: waffle_switch_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.waffle_switch_id_seq OWNED BY public.waffle_switch.id;


--
-- Name: account_emailaddress id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account_emailaddress ALTER COLUMN id SET DEFAULT nextval('public.account_emailaddress_id_seq'::regclass);


--
-- Name: account_emailconfirmation id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account_emailconfirmation ALTER COLUMN id SET DEFAULT nextval('public.account_emailconfirmation_id_seq'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: categories_category id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories_category ALTER COLUMN id SET DEFAULT nextval('public.categories_category_id_seq'::regclass);


--
-- Name: celery_taskmeta id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.celery_taskmeta ALTER COLUMN id SET DEFAULT nextval('public.celery_taskmeta_id_seq'::regclass);


--
-- Name: celery_tasksetmeta id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.celery_tasksetmeta ALTER COLUMN id SET DEFAULT nextval('public.celery_tasksetmeta_id_seq'::regclass);


--
-- Name: corsheaders_corsmodel id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.corsheaders_corsmodel ALTER COLUMN id SET DEFAULT nextval('public.corsheaders_corsmodel_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_celery_beat_crontabschedule id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_crontabschedule ALTER COLUMN id SET DEFAULT nextval('public.django_celery_beat_crontabschedule_id_seq'::regclass);


--
-- Name: django_celery_beat_intervalschedule id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_intervalschedule ALTER COLUMN id SET DEFAULT nextval('public.django_celery_beat_intervalschedule_id_seq'::regclass);


--
-- Name: django_celery_beat_periodictask id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_periodictask ALTER COLUMN id SET DEFAULT nextval('public.django_celery_beat_periodictask_id_seq'::regclass);


--
-- Name: django_celery_beat_solarschedule id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_solarschedule ALTER COLUMN id SET DEFAULT nextval('public.django_celery_beat_solarschedule_id_seq'::regclass);


--
-- Name: django_celery_results_taskresult id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_results_taskresult ALTER COLUMN id SET DEFAULT nextval('public.django_celery_results_taskresult_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: django_site id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_site ALTER COLUMN id SET DEFAULT nextval('public.django_site_id_seq'::regclass);


--
-- Name: djcelery_crontabschedule id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.djcelery_crontabschedule ALTER COLUMN id SET DEFAULT nextval('public.djcelery_crontabschedule_id_seq'::regclass);


--
-- Name: djcelery_intervalschedule id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.djcelery_intervalschedule ALTER COLUMN id SET DEFAULT nextval('public.djcelery_intervalschedule_id_seq'::regclass);


--
-- Name: djcelery_periodictask id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.djcelery_periodictask ALTER COLUMN id SET DEFAULT nextval('public.djcelery_periodictask_id_seq'::regclass);


--
-- Name: djcelery_taskstate id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.djcelery_taskstate ALTER COLUMN id SET DEFAULT nextval('public.djcelery_taskstate_id_seq'::regclass);


--
-- Name: djcelery_workerstate id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.djcelery_workerstate ALTER COLUMN id SET DEFAULT nextval('public.djcelery_workerstate_id_seq'::regclass);


--
-- Name: easy_thumbnails_source id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.easy_thumbnails_source ALTER COLUMN id SET DEFAULT nextval('public.easy_thumbnails_source_id_seq'::regclass);


--
-- Name: easy_thumbnails_thumbnail id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.easy_thumbnails_thumbnail ALTER COLUMN id SET DEFAULT nextval('public.easy_thumbnails_thumbnail_id_seq'::regclass);


--
-- Name: easy_thumbnails_thumbnaildimensions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.easy_thumbnails_thumbnaildimensions ALTER COLUMN id SET DEFAULT nextval('public.easy_thumbnails_thumbnaildimensions_id_seq'::regclass);


--
-- Name: environment_issuecheckconfig id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_issuecheckconfig ALTER COLUMN id SET DEFAULT nextval('public.environment_issuecheckconfig_id_seq'::regclass);


--
-- Name: environment_tenantflag id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantflag ALTER COLUMN id SET DEFAULT nextval('public.environment_tenantflag_id_seq'::regclass);


--
-- Name: environment_tenantflag_countries id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantflag_countries ALTER COLUMN id SET DEFAULT nextval('public.environment_tenantflag_countries_id_seq'::regclass);


--
-- Name: environment_tenantflag_groups id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantflag_groups ALTER COLUMN id SET DEFAULT nextval('public.environment_tenantflag_groups_id_seq'::regclass);


--
-- Name: environment_tenantflag_users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantflag_users ALTER COLUMN id SET DEFAULT nextval('public.environment_tenantflag_users_id_seq'::regclass);


--
-- Name: environment_tenantswitch id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantswitch ALTER COLUMN id SET DEFAULT nextval('public.environment_tenantswitch_id_seq'::regclass);


--
-- Name: environment_tenantswitch_countries id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantswitch_countries ALTER COLUMN id SET DEFAULT nextval('public.environment_tenantswitch_countries_id_seq'::regclass);


--
-- Name: filer_clipboard id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_clipboard ALTER COLUMN id SET DEFAULT nextval('public.filer_clipboard_id_seq'::regclass);


--
-- Name: filer_clipboarditem id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_clipboarditem ALTER COLUMN id SET DEFAULT nextval('public.filer_clipboarditem_id_seq'::regclass);


--
-- Name: filer_file id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_file ALTER COLUMN id SET DEFAULT nextval('public.filer_file_id_seq'::regclass);


--
-- Name: filer_folder id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_folder ALTER COLUMN id SET DEFAULT nextval('public.filer_folder_id_seq'::regclass);


--
-- Name: filer_folderpermission id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_folderpermission ALTER COLUMN id SET DEFAULT nextval('public.filer_folderpermission_id_seq'::regclass);


--
-- Name: generic_links_genericlink id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.generic_links_genericlink ALTER COLUMN id SET DEFAULT nextval('public.generic_links_genericlink_id_seq'::regclass);


--
-- Name: notification_notification id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_notification ALTER COLUMN id SET DEFAULT nextval('public.notification_notification_id_seq'::regclass);


--
-- Name: permissions2_permission id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permissions2_permission ALTER COLUMN id SET DEFAULT nextval('public.permissions2_permission_id_seq'::regclass);


--
-- Name: post_office_attachment id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_office_attachment ALTER COLUMN id SET DEFAULT nextval('public.post_office_attachment_id_seq'::regclass);


--
-- Name: post_office_attachment_emails id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_office_attachment_emails ALTER COLUMN id SET DEFAULT nextval('public.post_office_attachment_emails_id_seq'::regclass);


--
-- Name: post_office_email id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_office_email ALTER COLUMN id SET DEFAULT nextval('public.post_office_email_id_seq'::regclass);


--
-- Name: post_office_emailtemplate id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_office_emailtemplate ALTER COLUMN id SET DEFAULT nextval('public.post_office_emailtemplate_id_seq'::regclass);


--
-- Name: post_office_log id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_office_log ALTER COLUMN id SET DEFAULT nextval('public.post_office_log_id_seq'::regclass);


--
-- Name: publics_airlinecompany id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_airlinecompany ALTER COLUMN id SET DEFAULT nextval('public.publics_airlinecompany_id_seq'::regclass);


--
-- Name: publics_businessarea id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_businessarea ALTER COLUMN id SET DEFAULT nextval('public.publics_businessarea_id_seq'::regclass);


--
-- Name: publics_businessregion id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_businessregion ALTER COLUMN id SET DEFAULT nextval('public.publics_businessregion_id_seq'::regclass);


--
-- Name: publics_country id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_country ALTER COLUMN id SET DEFAULT nextval('public.publics_country_id_seq'::regclass);


--
-- Name: publics_currency id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_currency ALTER COLUMN id SET DEFAULT nextval('public.publics_currency_id_seq'::regclass);


--
-- Name: publics_dsarate id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_dsarate ALTER COLUMN id SET DEFAULT nextval('public.publics_dsarate_id_seq'::regclass);


--
-- Name: publics_dsarateupload id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_dsarateupload ALTER COLUMN id SET DEFAULT nextval('public.publics_dsarateupload_id_seq'::regclass);


--
-- Name: publics_dsaregion id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_dsaregion ALTER COLUMN id SET DEFAULT nextval('public.publics_dsaregion_id_seq'::regclass);


--
-- Name: publics_exchangerate id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_exchangerate ALTER COLUMN id SET DEFAULT nextval('public.publics_exchangerate_id_seq'::regclass);


--
-- Name: publics_fund id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_fund ALTER COLUMN id SET DEFAULT nextval('public.publics_fund_id_seq'::regclass);


--
-- Name: publics_grant id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_grant ALTER COLUMN id SET DEFAULT nextval('public.publics_grant_id_seq'::regclass);


--
-- Name: publics_grant_funds id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_grant_funds ALTER COLUMN id SET DEFAULT nextval('public.publics_grant_funds_id_seq'::regclass);


--
-- Name: publics_travelagent id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_travelagent ALTER COLUMN id SET DEFAULT nextval('public.publics_travelagent_id_seq'::regclass);


--
-- Name: publics_travelexpensetype id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_travelexpensetype ALTER COLUMN id SET DEFAULT nextval('public.publics_travelexpensetype_id_seq'::regclass);


--
-- Name: publics_wbs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_wbs ALTER COLUMN id SET DEFAULT nextval('public.publics_wbs_id_seq'::regclass);


--
-- Name: publics_wbs_grants id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_wbs_grants ALTER COLUMN id SET DEFAULT nextval('public.publics_wbs_grants_id_seq'::regclass);


--
-- Name: purchase_order_auditorfirm id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order_auditorfirm ALTER COLUMN id SET DEFAULT nextval('public.purchase_order_auditorfirm_id_seq'::regclass);


--
-- Name: purchase_order_auditorstaffmember id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order_auditorstaffmember ALTER COLUMN id SET DEFAULT nextval('public.purchase_order_auditorstaffmember_id_seq'::regclass);


--
-- Name: purchase_order_purchaseorder id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order_purchaseorder ALTER COLUMN id SET DEFAULT nextval('public.purchase_order_purchaseorder_id_seq'::regclass);


--
-- Name: purchase_order_purchaseorderitem id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order_purchaseorderitem ALTER COLUMN id SET DEFAULT nextval('public.purchase_order_purchaseorderitem_id_seq'::regclass);


--
-- Name: registration_registrationprofile id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registration_registrationprofile ALTER COLUMN id SET DEFAULT nextval('public.registration_registrationprofile_id_seq'::regclass);


--
-- Name: reversion_revision id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reversion_revision ALTER COLUMN id SET DEFAULT nextval('public.reversion_revision_id_seq'::regclass);


--
-- Name: reversion_version id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reversion_version ALTER COLUMN id SET DEFAULT nextval('public.reversion_version_id_seq'::regclass);


--
-- Name: socialaccount_socialaccount id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socialaccount_socialaccount ALTER COLUMN id SET DEFAULT nextval('public.socialaccount_socialaccount_id_seq'::regclass);


--
-- Name: socialaccount_socialapp id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socialaccount_socialapp ALTER COLUMN id SET DEFAULT nextval('public.socialaccount_socialapp_id_seq'::regclass);


--
-- Name: socialaccount_socialapp_sites id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites ALTER COLUMN id SET DEFAULT nextval('public.socialaccount_socialapp_sites_id_seq'::regclass);


--
-- Name: socialaccount_socialtoken id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socialaccount_socialtoken ALTER COLUMN id SET DEFAULT nextval('public.socialaccount_socialtoken_id_seq'::regclass);


--
-- Name: tpmpartners_tpmpartner id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tpmpartners_tpmpartner ALTER COLUMN id SET DEFAULT nextval('public.tpmpartners_tpmpartner_id_seq'::regclass);


--
-- Name: tpmpartners_tpmpartner_countries id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tpmpartners_tpmpartner_countries ALTER COLUMN id SET DEFAULT nextval('public.tpmpartners_tpmpartner_countries_id_seq'::regclass);


--
-- Name: tpmpartners_tpmpartnerstaffmember id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tpmpartners_tpmpartnerstaffmember ALTER COLUMN id SET DEFAULT nextval('public.tpmpartners_tpmpartnerstaffmember_id_seq'::regclass);


--
-- Name: unicef_notification_notification id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.unicef_notification_notification ALTER COLUMN id SET DEFAULT nextval('public.unicef_notification_notification_id_seq'::regclass);


--
-- Name: users_country id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_country ALTER COLUMN id SET DEFAULT nextval('public.users_country_id_seq'::regclass);


--
-- Name: users_country_offices id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_country_offices ALTER COLUMN id SET DEFAULT nextval('public.users_country_offices_id_seq'::regclass);


--
-- Name: users_office id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_office ALTER COLUMN id SET DEFAULT nextval('public.users_office_id_seq'::regclass);


--
-- Name: users_section id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_section ALTER COLUMN id SET DEFAULT nextval('public.users_section_id_seq'::regclass);


--
-- Name: users_userprofile id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_userprofile ALTER COLUMN id SET DEFAULT nextval('public.users_userprofile_id_seq'::regclass);


--
-- Name: users_userprofile_countries_available id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_userprofile_countries_available ALTER COLUMN id SET DEFAULT nextval('public.users_userprofile_countries_available_id_seq'::regclass);


--
-- Name: users_workspacecounter id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_workspacecounter ALTER COLUMN id SET DEFAULT nextval('public.users_workspacecounter_id_seq'::regclass);


--
-- Name: vision_visionsynclog id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vision_visionsynclog ALTER COLUMN id SET DEFAULT nextval('public.vision_visionsynclog_id_seq'::regclass);


--
-- Name: waffle_flag id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.waffle_flag ALTER COLUMN id SET DEFAULT nextval('public.waffle_flag_id_seq'::regclass);


--
-- Name: waffle_flag_groups id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.waffle_flag_groups ALTER COLUMN id SET DEFAULT nextval('public.waffle_flag_groups_id_seq'::regclass);


--
-- Name: waffle_flag_users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.waffle_flag_users ALTER COLUMN id SET DEFAULT nextval('public.waffle_flag_users_id_seq'::regclass);


--
-- Name: waffle_sample id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.waffle_sample ALTER COLUMN id SET DEFAULT nextval('public.waffle_sample_id_seq'::regclass);


--
-- Name: waffle_switch id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.waffle_switch ALTER COLUMN id SET DEFAULT nextval('public.waffle_switch_id_seq'::regclass);


--
-- Name: account_emailaddress account_emailaddress_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_email_key UNIQUE (email);


--
-- Name: account_emailaddress account_emailaddress_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_pkey PRIMARY KEY (id);


--
-- Name: account_emailconfirmation account_emailconfirmation_key_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirmation_key_key UNIQUE (key);


--
-- Name: account_emailconfirmation account_emailconfirmation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirmation_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user auth_user_email_1c89df09_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_email_1c89df09_uniq UNIQUE (email);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- Name: categories_category categories_category_description_453a5879_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories_category
    ADD CONSTRAINT categories_category_description_453a5879_uniq UNIQUE (description, module);


--
-- Name: categories_category categories_category_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories_category
    ADD CONSTRAINT categories_category_pkey PRIMARY KEY (id);


--
-- Name: celery_taskmeta celery_taskmeta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.celery_taskmeta
    ADD CONSTRAINT celery_taskmeta_pkey PRIMARY KEY (id);


--
-- Name: celery_taskmeta celery_taskmeta_task_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.celery_taskmeta
    ADD CONSTRAINT celery_taskmeta_task_id_key UNIQUE (task_id);


--
-- Name: celery_tasksetmeta celery_tasksetmeta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.celery_tasksetmeta
    ADD CONSTRAINT celery_tasksetmeta_pkey PRIMARY KEY (id);


--
-- Name: celery_tasksetmeta celery_tasksetmeta_taskset_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.celery_tasksetmeta
    ADD CONSTRAINT celery_tasksetmeta_taskset_id_key UNIQUE (taskset_id);


--
-- Name: corsheaders_corsmodel corsheaders_corsmodel_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.corsheaders_corsmodel
    ADD CONSTRAINT corsheaders_corsmodel_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_celery_beat_crontabschedule django_celery_beat_crontabschedule_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_crontabschedule
    ADD CONSTRAINT django_celery_beat_crontabschedule_pkey PRIMARY KEY (id);


--
-- Name: django_celery_beat_intervalschedule django_celery_beat_intervalschedule_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_intervalschedule
    ADD CONSTRAINT django_celery_beat_intervalschedule_pkey PRIMARY KEY (id);


--
-- Name: django_celery_beat_periodictask django_celery_beat_periodictask_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_periodictask
    ADD CONSTRAINT django_celery_beat_periodictask_name_key UNIQUE (name);


--
-- Name: django_celery_beat_periodictask django_celery_beat_periodictask_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_periodictask
    ADD CONSTRAINT django_celery_beat_periodictask_pkey PRIMARY KEY (id);


--
-- Name: django_celery_beat_periodictasks django_celery_beat_periodictasks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_periodictasks
    ADD CONSTRAINT django_celery_beat_periodictasks_pkey PRIMARY KEY (ident);


--
-- Name: django_celery_beat_solarschedule django_celery_beat_solarschedule_event_ba64999a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_solarschedule
    ADD CONSTRAINT django_celery_beat_solarschedule_event_ba64999a_uniq UNIQUE (event, latitude, longitude);


--
-- Name: django_celery_beat_solarschedule django_celery_beat_solarschedule_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_solarschedule
    ADD CONSTRAINT django_celery_beat_solarschedule_pkey PRIMARY KEY (id);


--
-- Name: django_celery_results_taskresult django_celery_results_taskresult_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_results_taskresult
    ADD CONSTRAINT django_celery_results_taskresult_pkey PRIMARY KEY (id);


--
-- Name: django_celery_results_taskresult django_celery_results_taskresult_task_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_results_taskresult
    ADD CONSTRAINT django_celery_results_taskresult_task_id_key UNIQUE (task_id);


--
-- Name: django_content_type django_content_type_app_label_45f3b1d93ec8c61c_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_45f3b1d93ec8c61c_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site django_site_domain_a2e37b91_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_domain_a2e37b91_uniq UNIQUE (domain);


--
-- Name: django_site django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: djcelery_crontabschedule djcelery_crontabschedule_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.djcelery_crontabschedule
    ADD CONSTRAINT djcelery_crontabschedule_pkey PRIMARY KEY (id);


--
-- Name: djcelery_intervalschedule djcelery_intervalschedule_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.djcelery_intervalschedule
    ADD CONSTRAINT djcelery_intervalschedule_pkey PRIMARY KEY (id);


--
-- Name: djcelery_periodictask djcelery_periodictask_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.djcelery_periodictask
    ADD CONSTRAINT djcelery_periodictask_name_key UNIQUE (name);


--
-- Name: djcelery_periodictask djcelery_periodictask_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.djcelery_periodictask
    ADD CONSTRAINT djcelery_periodictask_pkey PRIMARY KEY (id);


--
-- Name: djcelery_periodictasks djcelery_periodictasks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.djcelery_periodictasks
    ADD CONSTRAINT djcelery_periodictasks_pkey PRIMARY KEY (ident);


--
-- Name: djcelery_taskstate djcelery_taskstate_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.djcelery_taskstate
    ADD CONSTRAINT djcelery_taskstate_pkey PRIMARY KEY (id);


--
-- Name: djcelery_taskstate djcelery_taskstate_task_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.djcelery_taskstate
    ADD CONSTRAINT djcelery_taskstate_task_id_key UNIQUE (task_id);


--
-- Name: djcelery_workerstate djcelery_workerstate_hostname_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.djcelery_workerstate
    ADD CONSTRAINT djcelery_workerstate_hostname_key UNIQUE (hostname);


--
-- Name: djcelery_workerstate djcelery_workerstate_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.djcelery_workerstate
    ADD CONSTRAINT djcelery_workerstate_pkey PRIMARY KEY (id);


--
-- Name: drfpasswordless_callbacktoken drfpasswordless_callbacktoken_key_5814d2b6_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.drfpasswordless_callbacktoken
    ADD CONSTRAINT drfpasswordless_callbacktoken_key_5814d2b6_uniq UNIQUE (key, is_active);


--
-- Name: drfpasswordless_callbacktoken drfpasswordless_callbacktoken_key_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.drfpasswordless_callbacktoken
    ADD CONSTRAINT drfpasswordless_callbacktoken_key_key UNIQUE (key);


--
-- Name: drfpasswordless_callbacktoken drfpasswordless_callbacktoken_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.drfpasswordless_callbacktoken
    ADD CONSTRAINT drfpasswordless_callbacktoken_pkey PRIMARY KEY (id);


--
-- Name: easy_thumbnails_source easy_thumbnails_source_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.easy_thumbnails_source
    ADD CONSTRAINT easy_thumbnails_source_pkey PRIMARY KEY (id);


--
-- Name: easy_thumbnails_source easy_thumbnails_source_storage_hash_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.easy_thumbnails_source
    ADD CONSTRAINT easy_thumbnails_source_storage_hash_name_key UNIQUE (storage_hash, name);


--
-- Name: easy_thumbnails_thumbnail easy_thumbnails_thumbnail_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.easy_thumbnails_thumbnail
    ADD CONSTRAINT easy_thumbnails_thumbnail_pkey PRIMARY KEY (id);


--
-- Name: easy_thumbnails_thumbnail easy_thumbnails_thumbnail_storage_hash_name_source_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.easy_thumbnails_thumbnail
    ADD CONSTRAINT easy_thumbnails_thumbnail_storage_hash_name_source_id_key UNIQUE (storage_hash, name, source_id);


--
-- Name: easy_thumbnails_thumbnaildimensions easy_thumbnails_thumbnaildimensions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.easy_thumbnails_thumbnaildimensions
    ADD CONSTRAINT easy_thumbnails_thumbnaildimensions_pkey PRIMARY KEY (id);


--
-- Name: easy_thumbnails_thumbnaildimensions easy_thumbnails_thumbnaildimensions_thumbnail_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.easy_thumbnails_thumbnaildimensions
    ADD CONSTRAINT easy_thumbnails_thumbnaildimensions_thumbnail_id_key UNIQUE (thumbnail_id);


--
-- Name: environment_issuecheckconfig environment_issuecheckconfig_check_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_issuecheckconfig
    ADD CONSTRAINT environment_issuecheckconfig_check_id_key UNIQUE (check_id);


--
-- Name: environment_issuecheckconfig environment_issuecheckconfig_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_issuecheckconfig
    ADD CONSTRAINT environment_issuecheckconfig_pkey PRIMARY KEY (id);


--
-- Name: environment_tenantflag_countries environment_tenantflag_countries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantflag_countries
    ADD CONSTRAINT environment_tenantflag_countries_pkey PRIMARY KEY (id);


--
-- Name: environment_tenantflag_countries environment_tenantflag_countries_tenantflag_id_5562563c_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantflag_countries
    ADD CONSTRAINT environment_tenantflag_countries_tenantflag_id_5562563c_uniq UNIQUE (tenantflag_id, country_id);


--
-- Name: environment_tenantflag_groups environment_tenantflag_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantflag_groups
    ADD CONSTRAINT environment_tenantflag_groups_pkey PRIMARY KEY (id);


--
-- Name: environment_tenantflag_groups environment_tenantflag_groups_tenantflag_id_e706e7a5_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantflag_groups
    ADD CONSTRAINT environment_tenantflag_groups_tenantflag_id_e706e7a5_uniq UNIQUE (tenantflag_id, group_id);


--
-- Name: environment_tenantflag environment_tenantflag_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantflag
    ADD CONSTRAINT environment_tenantflag_name_key UNIQUE (name);


--
-- Name: environment_tenantflag environment_tenantflag_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantflag
    ADD CONSTRAINT environment_tenantflag_pkey PRIMARY KEY (id);


--
-- Name: environment_tenantflag_users environment_tenantflag_users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantflag_users
    ADD CONSTRAINT environment_tenantflag_users_pkey PRIMARY KEY (id);


--
-- Name: environment_tenantflag_users environment_tenantflag_users_tenantflag_id_4518c0a6_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantflag_users
    ADD CONSTRAINT environment_tenantflag_users_tenantflag_id_4518c0a6_uniq UNIQUE (tenantflag_id, user_id);


--
-- Name: environment_tenantswitch_countries environment_tenantswitch_countrie_tenantswitch_id_f9d7e039_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantswitch_countries
    ADD CONSTRAINT environment_tenantswitch_countrie_tenantswitch_id_f9d7e039_uniq UNIQUE (tenantswitch_id, country_id);


--
-- Name: environment_tenantswitch_countries environment_tenantswitch_countries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantswitch_countries
    ADD CONSTRAINT environment_tenantswitch_countries_pkey PRIMARY KEY (id);


--
-- Name: environment_tenantswitch environment_tenantswitch_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantswitch
    ADD CONSTRAINT environment_tenantswitch_name_key UNIQUE (name);


--
-- Name: environment_tenantswitch environment_tenantswitch_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantswitch
    ADD CONSTRAINT environment_tenantswitch_pkey PRIMARY KEY (id);


--
-- Name: filer_clipboard filer_clipboard_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_clipboard
    ADD CONSTRAINT filer_clipboard_pkey PRIMARY KEY (id);


--
-- Name: filer_clipboarditem filer_clipboarditem_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_clipboarditem
    ADD CONSTRAINT filer_clipboarditem_pkey PRIMARY KEY (id);


--
-- Name: filer_file filer_file_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_file
    ADD CONSTRAINT filer_file_pkey PRIMARY KEY (id);


--
-- Name: filer_folder filer_folder_parent_id_30ad83e34d901e49_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_folder
    ADD CONSTRAINT filer_folder_parent_id_30ad83e34d901e49_uniq UNIQUE (parent_id, name);


--
-- Name: filer_folder filer_folder_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_folder
    ADD CONSTRAINT filer_folder_pkey PRIMARY KEY (id);


--
-- Name: filer_folderpermission filer_folderpermission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_folderpermission
    ADD CONSTRAINT filer_folderpermission_pkey PRIMARY KEY (id);


--
-- Name: filer_image filer_image_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_image
    ADD CONSTRAINT filer_image_pkey PRIMARY KEY (file_ptr_id);


--
-- Name: generic_links_genericlink generic_links_genericlink_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.generic_links_genericlink
    ADD CONSTRAINT generic_links_genericlink_pkey PRIMARY KEY (id);


--
-- Name: notification_notification notification_notification_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_notification
    ADD CONSTRAINT notification_notification_pkey PRIMARY KEY (id);


--
-- Name: permissions2_permission permissions2_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permissions2_permission
    ADD CONSTRAINT permissions2_permission_pkey PRIMARY KEY (id);


--
-- Name: post_office_attachment_emails post_office_attachment_emails_attachment_id_email_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_office_attachment_emails
    ADD CONSTRAINT post_office_attachment_emails_attachment_id_email_id_key UNIQUE (attachment_id, email_id);


--
-- Name: post_office_attachment_emails post_office_attachment_emails_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_office_attachment_emails
    ADD CONSTRAINT post_office_attachment_emails_pkey PRIMARY KEY (id);


--
-- Name: post_office_attachment post_office_attachment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_office_attachment
    ADD CONSTRAINT post_office_attachment_pkey PRIMARY KEY (id);


--
-- Name: post_office_email post_office_email_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_office_email
    ADD CONSTRAINT post_office_email_pkey PRIMARY KEY (id);


--
-- Name: post_office_emailtemplate post_office_emailtemplate_name_4023e3e4_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_office_emailtemplate
    ADD CONSTRAINT post_office_emailtemplate_name_4023e3e4_uniq UNIQUE (name, language, default_template_id);


--
-- Name: post_office_emailtemplate post_office_emailtemplate_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_office_emailtemplate
    ADD CONSTRAINT post_office_emailtemplate_pkey PRIMARY KEY (id);


--
-- Name: post_office_log post_office_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_office_log
    ADD CONSTRAINT post_office_log_pkey PRIMARY KEY (id);


--
-- Name: publics_airlinecompany publics_airlinecompany_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_airlinecompany
    ADD CONSTRAINT publics_airlinecompany_pkey PRIMARY KEY (id);


--
-- Name: publics_businessarea publics_businessarea_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_businessarea
    ADD CONSTRAINT publics_businessarea_pkey PRIMARY KEY (id);


--
-- Name: publics_businessregion publics_businessregion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_businessregion
    ADD CONSTRAINT publics_businessregion_pkey PRIMARY KEY (id);


--
-- Name: publics_country publics_country_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_country
    ADD CONSTRAINT publics_country_pkey PRIMARY KEY (id);


--
-- Name: publics_country publics_country_vision_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_country
    ADD CONSTRAINT publics_country_vision_code_key UNIQUE (vision_code);


--
-- Name: publics_currency publics_currency_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_currency
    ADD CONSTRAINT publics_currency_pkey PRIMARY KEY (id);


--
-- Name: publics_dsarate publics_dsarate_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_dsarate
    ADD CONSTRAINT publics_dsarate_pkey PRIMARY KEY (id);


--
-- Name: publics_dsarate publics_dsarate_region_id_fb084b2f_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_dsarate
    ADD CONSTRAINT publics_dsarate_region_id_fb084b2f_uniq UNIQUE (region_id, effective_to_date);


--
-- Name: publics_dsarateupload publics_dsarateupload_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_dsarateupload
    ADD CONSTRAINT publics_dsarateupload_pkey PRIMARY KEY (id);


--
-- Name: publics_dsaregion publics_dsaregion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_dsaregion
    ADD CONSTRAINT publics_dsaregion_pkey PRIMARY KEY (id);


--
-- Name: publics_exchangerate publics_exchangerate_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_exchangerate
    ADD CONSTRAINT publics_exchangerate_pkey PRIMARY KEY (id);


--
-- Name: publics_fund publics_fund_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_fund
    ADD CONSTRAINT publics_fund_pkey PRIMARY KEY (id);


--
-- Name: publics_grant_funds publics_grant_funds_grant_id_89d49dbd_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_grant_funds
    ADD CONSTRAINT publics_grant_funds_grant_id_89d49dbd_uniq UNIQUE (grant_id, fund_id);


--
-- Name: publics_grant_funds publics_grant_funds_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_grant_funds
    ADD CONSTRAINT publics_grant_funds_pkey PRIMARY KEY (id);


--
-- Name: publics_grant publics_grant_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_grant
    ADD CONSTRAINT publics_grant_pkey PRIMARY KEY (id);


--
-- Name: publics_travelagent publics_travelagent_expense_type_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_travelagent
    ADD CONSTRAINT publics_travelagent_expense_type_id_key UNIQUE (expense_type_id);


--
-- Name: publics_travelagent publics_travelagent_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_travelagent
    ADD CONSTRAINT publics_travelagent_pkey PRIMARY KEY (id);


--
-- Name: publics_travelexpensetype publics_travelexpensetype_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_travelexpensetype
    ADD CONSTRAINT publics_travelexpensetype_pkey PRIMARY KEY (id);


--
-- Name: publics_wbs_grants publics_wbs_grants_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_wbs_grants
    ADD CONSTRAINT publics_wbs_grants_pkey PRIMARY KEY (id);


--
-- Name: publics_wbs_grants publics_wbs_grants_wbs_id_239adc1b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_wbs_grants
    ADD CONSTRAINT publics_wbs_grants_wbs_id_239adc1b_uniq UNIQUE (wbs_id, grant_id);


--
-- Name: publics_wbs publics_wbs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_wbs
    ADD CONSTRAINT publics_wbs_pkey PRIMARY KEY (id);


--
-- Name: purchase_order_auditorfirm purchase_order_auditorfirm_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order_auditorfirm
    ADD CONSTRAINT purchase_order_auditorfirm_pkey PRIMARY KEY (id);


--
-- Name: purchase_order_auditorfirm purchase_order_auditorfirm_vendor_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order_auditorfirm
    ADD CONSTRAINT purchase_order_auditorfirm_vendor_number_key UNIQUE (vendor_number);


--
-- Name: purchase_order_auditorstaffmember purchase_order_auditorstaffmember_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order_auditorstaffmember
    ADD CONSTRAINT purchase_order_auditorstaffmember_pkey PRIMARY KEY (id);


--
-- Name: purchase_order_auditorstaffmember purchase_order_auditorstaffmember_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order_auditorstaffmember
    ADD CONSTRAINT purchase_order_auditorstaffmember_user_id_key UNIQUE (user_id);


--
-- Name: purchase_order_purchaseorder purchase_order_purchaseorder_order_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order_purchaseorder
    ADD CONSTRAINT purchase_order_purchaseorder_order_number_key UNIQUE (order_number);


--
-- Name: purchase_order_purchaseorder purchase_order_purchaseorder_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order_purchaseorder
    ADD CONSTRAINT purchase_order_purchaseorder_pkey PRIMARY KEY (id);


--
-- Name: purchase_order_purchaseorderitem purchase_order_purchaseorderite_purchase_order_id_d3c58c7f_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order_purchaseorderitem
    ADD CONSTRAINT purchase_order_purchaseorderite_purchase_order_id_d3c58c7f_uniq UNIQUE (purchase_order_id, number);


--
-- Name: purchase_order_purchaseorderitem purchase_order_purchaseorderitem_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order_purchaseorderitem
    ADD CONSTRAINT purchase_order_purchaseorderitem_pkey PRIMARY KEY (id);


--
-- Name: registration_emailregistrationprofile registration_emailregistrationprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registration_emailregistrationprofile
    ADD CONSTRAINT registration_emailregistrationprofile_pkey PRIMARY KEY (registrationprofile_ptr_id);


--
-- Name: registration_registrationprofile registration_registrationprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registration_registrationprofile
    ADD CONSTRAINT registration_registrationprofile_pkey PRIMARY KEY (id);


--
-- Name: registration_registrationprofile registration_registrationprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registration_registrationprofile
    ADD CONSTRAINT registration_registrationprofile_user_id_key UNIQUE (user_id);


--
-- Name: reversion_revision reversion_revision_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reversion_revision
    ADD CONSTRAINT reversion_revision_pkey PRIMARY KEY (id);


--
-- Name: reversion_version reversion_version_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reversion_version
    ADD CONSTRAINT reversion_version_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialaccount socialaccount_socialaccount_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialaccount socialaccount_socialaccount_provider_36eec1734f431f56_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_provider_36eec1734f431f56_uniq UNIQUE (provider, uid);


--
-- Name: socialaccount_socialapp socialaccount_socialapp_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socialaccount_socialapp
    ADD CONSTRAINT socialaccount_socialapp_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialapp_sites socialaccount_socialapp_sites_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_socialapp_sites_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialapp_sites socialaccount_socialapp_sites_socialapp_id_site_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_socialapp_sites_socialapp_id_site_id_key UNIQUE (socialapp_id, site_id);


--
-- Name: socialaccount_socialtoken socialaccount_socialtoken_app_id_697928748c2e1968_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_socialtoken_app_id_697928748c2e1968_uniq UNIQUE (app_id, account_id);


--
-- Name: socialaccount_socialtoken socialaccount_socialtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_socialtoken_pkey PRIMARY KEY (id);


--
-- Name: tpmpartners_tpmpartner_countries tpmpartners_tpmpartner_countries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tpmpartners_tpmpartner_countries
    ADD CONSTRAINT tpmpartners_tpmpartner_countries_pkey PRIMARY KEY (id);


--
-- Name: tpmpartners_tpmpartner_countries tpmpartners_tpmpartner_countries_tpmpartner_id_969975f4_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tpmpartners_tpmpartner_countries
    ADD CONSTRAINT tpmpartners_tpmpartner_countries_tpmpartner_id_969975f4_uniq UNIQUE (tpmpartner_id, country_id);


--
-- Name: tpmpartners_tpmpartner tpmpartners_tpmpartner_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tpmpartners_tpmpartner
    ADD CONSTRAINT tpmpartners_tpmpartner_pkey PRIMARY KEY (id);


--
-- Name: tpmpartners_tpmpartner tpmpartners_tpmpartner_vendor_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tpmpartners_tpmpartner
    ADD CONSTRAINT tpmpartners_tpmpartner_vendor_number_key UNIQUE (vendor_number);


--
-- Name: tpmpartners_tpmpartnerstaffmember tpmpartners_tpmpartnerstaffmember_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tpmpartners_tpmpartnerstaffmember
    ADD CONSTRAINT tpmpartners_tpmpartnerstaffmember_pkey PRIMARY KEY (id);


--
-- Name: tpmpartners_tpmpartnerstaffmember tpmpartners_tpmpartnerstaffmember_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tpmpartners_tpmpartnerstaffmember
    ADD CONSTRAINT tpmpartners_tpmpartnerstaffmember_user_id_key UNIQUE (user_id);


--
-- Name: unicef_notification_notification unicef_notification_notification_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.unicef_notification_notification
    ADD CONSTRAINT unicef_notification_notification_pkey PRIMARY KEY (id);


--
-- Name: users_country users_country_domain_url_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_country
    ADD CONSTRAINT users_country_domain_url_key UNIQUE (domain_url);


--
-- Name: users_country_offices users_country_offices_country_id_office_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_country_offices
    ADD CONSTRAINT users_country_offices_country_id_office_id_key UNIQUE (country_id, office_id);


--
-- Name: users_country_offices users_country_offices_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_country_offices
    ADD CONSTRAINT users_country_offices_pkey PRIMARY KEY (id);


--
-- Name: users_country users_country_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_country
    ADD CONSTRAINT users_country_pkey PRIMARY KEY (id);


--
-- Name: users_country users_country_schema_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_country
    ADD CONSTRAINT users_country_schema_name_key UNIQUE (schema_name);


--
-- Name: users_equitrackregistrationmodel users_equitrackregistrationmodel_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_equitrackregistrationmodel
    ADD CONSTRAINT users_equitrackregistrationmodel_pkey PRIMARY KEY (registrationprofile_ptr_id);


--
-- Name: users_office users_office_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_office
    ADD CONSTRAINT users_office_pkey PRIMARY KEY (id);


--
-- Name: users_section users_section_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_section
    ADD CONSTRAINT users_section_code_key UNIQUE (code);


--
-- Name: users_section users_section_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_section
    ADD CONSTRAINT users_section_name_key UNIQUE (name);


--
-- Name: users_section users_section_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_section
    ADD CONSTRAINT users_section_pkey PRIMARY KEY (id);


--
-- Name: users_userprofile_countries_available users_userprofile_countries_avail_userprofile_id_country_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_userprofile_countries_available
    ADD CONSTRAINT users_userprofile_countries_avail_userprofile_id_country_id_key UNIQUE (userprofile_id, country_id);


--
-- Name: users_userprofile_countries_available users_userprofile_countries_available_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_userprofile_countries_available
    ADD CONSTRAINT users_userprofile_countries_available_pkey PRIMARY KEY (id);


--
-- Name: users_userprofile users_userprofile_guid_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofile_guid_key UNIQUE (guid);


--
-- Name: users_userprofile users_userprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofile_pkey PRIMARY KEY (id);


--
-- Name: users_userprofile users_userprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofile_user_id_key UNIQUE (user_id);


--
-- Name: users_userprofile users_userprofile_vendor_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofile_vendor_number_key UNIQUE (vendor_number);


--
-- Name: users_workspacecounter users_workspacecounter_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_workspacecounter
    ADD CONSTRAINT users_workspacecounter_pkey PRIMARY KEY (id);


--
-- Name: users_workspacecounter users_workspacecounter_workspace_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_workspacecounter
    ADD CONSTRAINT users_workspacecounter_workspace_id_key UNIQUE (workspace_id);


--
-- Name: vision_visionsynclog vision_visionsynclog_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vision_visionsynclog
    ADD CONSTRAINT vision_visionsynclog_pkey PRIMARY KEY (id);


--
-- Name: waffle_flag_groups waffle_flag_groups_flag_id_8ba0c71b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.waffle_flag_groups
    ADD CONSTRAINT waffle_flag_groups_flag_id_8ba0c71b_uniq UNIQUE (flag_id, group_id);


--
-- Name: waffle_flag_groups waffle_flag_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.waffle_flag_groups
    ADD CONSTRAINT waffle_flag_groups_pkey PRIMARY KEY (id);


--
-- Name: waffle_flag waffle_flag_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.waffle_flag
    ADD CONSTRAINT waffle_flag_name_key UNIQUE (name);


--
-- Name: waffle_flag waffle_flag_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.waffle_flag
    ADD CONSTRAINT waffle_flag_pkey PRIMARY KEY (id);


--
-- Name: waffle_flag_users waffle_flag_users_flag_id_b46f76b0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.waffle_flag_users
    ADD CONSTRAINT waffle_flag_users_flag_id_b46f76b0_uniq UNIQUE (flag_id, user_id);


--
-- Name: waffle_flag_users waffle_flag_users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.waffle_flag_users
    ADD CONSTRAINT waffle_flag_users_pkey PRIMARY KEY (id);


--
-- Name: waffle_sample waffle_sample_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.waffle_sample
    ADD CONSTRAINT waffle_sample_name_key UNIQUE (name);


--
-- Name: waffle_sample waffle_sample_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.waffle_sample
    ADD CONSTRAINT waffle_sample_pkey PRIMARY KEY (id);


--
-- Name: waffle_switch waffle_switch_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.waffle_switch
    ADD CONSTRAINT waffle_switch_name_key UNIQUE (name);


--
-- Name: waffle_switch waffle_switch_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.waffle_switch
    ADD CONSTRAINT waffle_switch_pkey PRIMARY KEY (id);


--
-- Name: account_emailaddress_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX account_emailaddress_e8701ad4 ON public.account_emailaddress USING btree (user_id);


--
-- Name: account_emailaddress_email_206527469d8e1918_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX account_emailaddress_email_206527469d8e1918_like ON public.account_emailaddress USING btree (email varchar_pattern_ops);


--
-- Name: account_emailconfirmation_6f1edeac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX account_emailconfirmation_6f1edeac ON public.account_emailconfirmation USING btree (email_address_id);


--
-- Name: account_emailconfirmation_key_7033a271201d424f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX account_emailconfirmation_key_7033a271201d424f_like ON public.account_emailconfirmation USING btree (key varchar_pattern_ops);


--
-- Name: auth_group_name_253ae2a6331666e8_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_name_253ae2a6331666e8_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_0e939a4f ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_8373b171 ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_permission_417f1b1c ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_email_1c89df09_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_email_1c89df09_like ON public.auth_user USING btree (email varchar_pattern_ops);


--
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_groups_0e939a4f ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_groups_e8701ad4 ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_user_permissions_8373b171 ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_51b3b110094b8aae_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_username_51b3b110094b8aae_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: authtoken_token_key_7222ec672cd32dcd_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX authtoken_token_key_7222ec672cd32dcd_like ON public.authtoken_token USING btree (key varchar_pattern_ops);


--
-- Name: categories_category_70a17ffa; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX categories_category_70a17ffa ON public.categories_category USING btree ("order");


--
-- Name: celery_taskmeta_hidden; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX celery_taskmeta_hidden ON public.celery_taskmeta USING btree (hidden);


--
-- Name: celery_taskmeta_task_id_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX celery_taskmeta_task_id_like ON public.celery_taskmeta USING btree (task_id varchar_pattern_ops);


--
-- Name: celery_tasksetmeta_hidden; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX celery_tasksetmeta_hidden ON public.celery_tasksetmeta USING btree (hidden);


--
-- Name: celery_tasksetmeta_taskset_id_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX celery_tasksetmeta_taskset_id_like ON public.celery_tasksetmeta USING btree (taskset_id varchar_pattern_ops);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_417f1b1c ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_e8701ad4 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_celery_beat_periodictask_1dcd7040; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_celery_beat_periodictask_1dcd7040 ON public.django_celery_beat_periodictask USING btree (interval_id);


--
-- Name: django_celery_beat_periodictask_9a874ea8; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_celery_beat_periodictask_9a874ea8 ON public.django_celery_beat_periodictask USING btree (solar_id);


--
-- Name: django_celery_beat_periodictask_f3f0d72a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_celery_beat_periodictask_f3f0d72a ON public.django_celery_beat_periodictask USING btree (crontab_id);


--
-- Name: django_celery_beat_periodictask_name_265a36b7_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_celery_beat_periodictask_name_265a36b7_like ON public.django_celery_beat_periodictask USING btree (name varchar_pattern_ops);


--
-- Name: django_celery_results_taskresult_662f707d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_celery_results_taskresult_662f707d ON public.django_celery_results_taskresult USING btree (hidden);


--
-- Name: django_celery_results_taskresult_task_id_de0d95bf_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_celery_results_taskresult_task_id_de0d95bf_like ON public.django_celery_results_taskresult USING btree (task_id varchar_pattern_ops);


--
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_de54fa62 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_461cfeaa630ca218_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_session_key_461cfeaa630ca218_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: django_site_domain_a2e37b91_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_site_domain_a2e37b91_like ON public.django_site USING btree (domain varchar_pattern_ops);


--
-- Name: djcelery_periodictask_crontab_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX djcelery_periodictask_crontab_id ON public.djcelery_periodictask USING btree (crontab_id);


--
-- Name: djcelery_periodictask_interval_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX djcelery_periodictask_interval_id ON public.djcelery_periodictask USING btree (interval_id);


--
-- Name: djcelery_periodictask_name_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX djcelery_periodictask_name_like ON public.djcelery_periodictask USING btree (name varchar_pattern_ops);


--
-- Name: djcelery_taskstate_hidden; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX djcelery_taskstate_hidden ON public.djcelery_taskstate USING btree (hidden);


--
-- Name: djcelery_taskstate_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX djcelery_taskstate_name ON public.djcelery_taskstate USING btree (name);


--
-- Name: djcelery_taskstate_name_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX djcelery_taskstate_name_like ON public.djcelery_taskstate USING btree (name varchar_pattern_ops);


--
-- Name: djcelery_taskstate_state; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX djcelery_taskstate_state ON public.djcelery_taskstate USING btree (state);


--
-- Name: djcelery_taskstate_state_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX djcelery_taskstate_state_like ON public.djcelery_taskstate USING btree (state varchar_pattern_ops);


--
-- Name: djcelery_taskstate_task_id_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX djcelery_taskstate_task_id_like ON public.djcelery_taskstate USING btree (task_id varchar_pattern_ops);


--
-- Name: djcelery_taskstate_tstamp; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX djcelery_taskstate_tstamp ON public.djcelery_taskstate USING btree (tstamp);


--
-- Name: djcelery_taskstate_worker_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX djcelery_taskstate_worker_id ON public.djcelery_taskstate USING btree (worker_id);


--
-- Name: djcelery_workerstate_hostname_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX djcelery_workerstate_hostname_like ON public.djcelery_workerstate USING btree (hostname varchar_pattern_ops);


--
-- Name: djcelery_workerstate_last_heartbeat; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX djcelery_workerstate_last_heartbeat ON public.djcelery_workerstate USING btree (last_heartbeat);


--
-- Name: drfpasswordless_callbacktoken_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX drfpasswordless_callbacktoken_e8701ad4 ON public.drfpasswordless_callbacktoken USING btree (user_id);


--
-- Name: drfpasswordless_callbacktoken_key_1dd35a07_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX drfpasswordless_callbacktoken_key_1dd35a07_like ON public.drfpasswordless_callbacktoken USING btree (key varchar_pattern_ops);


--
-- Name: easy_thumbnails_source_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX easy_thumbnails_source_name ON public.easy_thumbnails_source USING btree (name);


--
-- Name: easy_thumbnails_source_name_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX easy_thumbnails_source_name_like ON public.easy_thumbnails_source USING btree (name varchar_pattern_ops);


--
-- Name: easy_thumbnails_source_storage_hash; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX easy_thumbnails_source_storage_hash ON public.easy_thumbnails_source USING btree (storage_hash);


--
-- Name: easy_thumbnails_source_storage_hash_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX easy_thumbnails_source_storage_hash_like ON public.easy_thumbnails_source USING btree (storage_hash varchar_pattern_ops);


--
-- Name: easy_thumbnails_thumbnail_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX easy_thumbnails_thumbnail_name ON public.easy_thumbnails_thumbnail USING btree (name);


--
-- Name: easy_thumbnails_thumbnail_name_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX easy_thumbnails_thumbnail_name_like ON public.easy_thumbnails_thumbnail USING btree (name varchar_pattern_ops);


--
-- Name: easy_thumbnails_thumbnail_source_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX easy_thumbnails_thumbnail_source_id ON public.easy_thumbnails_thumbnail USING btree (source_id);


--
-- Name: easy_thumbnails_thumbnail_storage_hash; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX easy_thumbnails_thumbnail_storage_hash ON public.easy_thumbnails_thumbnail USING btree (storage_hash);


--
-- Name: easy_thumbnails_thumbnail_storage_hash_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX easy_thumbnails_thumbnail_storage_hash_like ON public.easy_thumbnails_thumbnail USING btree (storage_hash varchar_pattern_ops);


--
-- Name: environment_issuecheckconfig_check_id_916cd0dd_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX environment_issuecheckconfig_check_id_916cd0dd_like ON public.environment_issuecheckconfig USING btree (check_id varchar_pattern_ops);


--
-- Name: environment_tenantflag_countries_818ea15e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX environment_tenantflag_countries_818ea15e ON public.environment_tenantflag_countries USING btree (tenantflag_id);


--
-- Name: environment_tenantflag_countries_93bfec8a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX environment_tenantflag_countries_93bfec8a ON public.environment_tenantflag_countries USING btree (country_id);


--
-- Name: environment_tenantflag_e2fa5388; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX environment_tenantflag_e2fa5388 ON public.environment_tenantflag USING btree (created);


--
-- Name: environment_tenantflag_groups_0e939a4f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX environment_tenantflag_groups_0e939a4f ON public.environment_tenantflag_groups USING btree (group_id);


--
-- Name: environment_tenantflag_groups_818ea15e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX environment_tenantflag_groups_818ea15e ON public.environment_tenantflag_groups USING btree (tenantflag_id);


--
-- Name: environment_tenantflag_name_f2788a9e_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX environment_tenantflag_name_f2788a9e_like ON public.environment_tenantflag USING btree (name varchar_pattern_ops);


--
-- Name: environment_tenantflag_users_818ea15e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX environment_tenantflag_users_818ea15e ON public.environment_tenantflag_users USING btree (tenantflag_id);


--
-- Name: environment_tenantflag_users_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX environment_tenantflag_users_e8701ad4 ON public.environment_tenantflag_users USING btree (user_id);


--
-- Name: environment_tenantswitch_countries_93bfec8a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX environment_tenantswitch_countries_93bfec8a ON public.environment_tenantswitch_countries USING btree (country_id);


--
-- Name: environment_tenantswitch_countries_f3e188b3; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX environment_tenantswitch_countries_f3e188b3 ON public.environment_tenantswitch_countries USING btree (tenantswitch_id);


--
-- Name: environment_tenantswitch_e2fa5388; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX environment_tenantswitch_e2fa5388 ON public.environment_tenantswitch USING btree (created);


--
-- Name: environment_tenantswitch_name_0a0c7d17_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX environment_tenantswitch_name_0a0c7d17_like ON public.environment_tenantswitch USING btree (name varchar_pattern_ops);


--
-- Name: filer_clipboard_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX filer_clipboard_e8701ad4 ON public.filer_clipboard USING btree (user_id);


--
-- Name: filer_clipboarditem_2655b062; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX filer_clipboarditem_2655b062 ON public.filer_clipboarditem USING btree (clipboard_id);


--
-- Name: filer_clipboarditem_814552b9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX filer_clipboarditem_814552b9 ON public.filer_clipboarditem USING btree (file_id);


--
-- Name: filer_file_5e7b1936; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX filer_file_5e7b1936 ON public.filer_file USING btree (owner_id);


--
-- Name: filer_file_a8a44dbb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX filer_file_a8a44dbb ON public.filer_file USING btree (folder_id);


--
-- Name: filer_file_d3e32c49; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX filer_file_d3e32c49 ON public.filer_file USING btree (polymorphic_ctype_id);


--
-- Name: filer_folder_3cfbd988; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX filer_folder_3cfbd988 ON public.filer_folder USING btree (rght);


--
-- Name: filer_folder_5e7b1936; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX filer_folder_5e7b1936 ON public.filer_folder USING btree (owner_id);


--
-- Name: filer_folder_656442a0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX filer_folder_656442a0 ON public.filer_folder USING btree (tree_id);


--
-- Name: filer_folder_6be37982; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX filer_folder_6be37982 ON public.filer_folder USING btree (parent_id);


--
-- Name: filer_folder_c9e9a848; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX filer_folder_c9e9a848 ON public.filer_folder USING btree (level);


--
-- Name: filer_folder_caf7cc51; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX filer_folder_caf7cc51 ON public.filer_folder USING btree (lft);


--
-- Name: filer_folderpermission_0e939a4f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX filer_folderpermission_0e939a4f ON public.filer_folderpermission USING btree (group_id);


--
-- Name: filer_folderpermission_a8a44dbb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX filer_folderpermission_a8a44dbb ON public.filer_folderpermission USING btree (folder_id);


--
-- Name: filer_folderpermission_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX filer_folderpermission_e8701ad4 ON public.filer_folderpermission USING btree (user_id);


--
-- Name: generic_links_genericlink_content_type_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX generic_links_genericlink_content_type_id ON public.generic_links_genericlink USING btree (content_type_id);


--
-- Name: generic_links_genericlink_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX generic_links_genericlink_created_at ON public.generic_links_genericlink USING btree (created_at);


--
-- Name: generic_links_genericlink_is_external; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX generic_links_genericlink_is_external ON public.generic_links_genericlink USING btree (is_external);


--
-- Name: generic_links_genericlink_object_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX generic_links_genericlink_object_id ON public.generic_links_genericlink USING btree (object_id);


--
-- Name: generic_links_genericlink_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX generic_links_genericlink_user_id ON public.generic_links_genericlink USING btree (user_id);


--
-- Name: notification_notification_417f1b1c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX notification_notification_417f1b1c ON public.notification_notification USING btree (content_type_id);


--
-- Name: notification_notification_f237b53f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX notification_notification_f237b53f ON public.notification_notification USING btree (sent_email_id);


--
-- Name: post_office_attachment_emails_07ba63f5; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX post_office_attachment_emails_07ba63f5 ON public.post_office_attachment_emails USING btree (attachment_id);


--
-- Name: post_office_attachment_emails_fdfd0ebf; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX post_office_attachment_emails_fdfd0ebf ON public.post_office_attachment_emails USING btree (email_id);


--
-- Name: post_office_email_3acc0b7a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX post_office_email_3acc0b7a ON public.post_office_email USING btree (last_updated);


--
-- Name: post_office_email_74f53564; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX post_office_email_74f53564 ON public.post_office_email USING btree (template_id);


--
-- Name: post_office_email_9acb4454; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX post_office_email_9acb4454 ON public.post_office_email USING btree (status);


--
-- Name: post_office_email_e2fa5388; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX post_office_email_e2fa5388 ON public.post_office_email USING btree (created);


--
-- Name: post_office_email_ed24d584; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX post_office_email_ed24d584 ON public.post_office_email USING btree (scheduled_time);


--
-- Name: post_office_emailtemplate_dea6f63e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX post_office_emailtemplate_dea6f63e ON public.post_office_emailtemplate USING btree (default_template_id);


--
-- Name: post_office_log_fdfd0ebf; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX post_office_log_fdfd0ebf ON public.post_office_log USING btree (email_id);


--
-- Name: publics_businessarea_0f442f96; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX publics_businessarea_0f442f96 ON public.publics_businessarea USING btree (region_id);


--
-- Name: publics_businessarea_ca761476; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX publics_businessarea_ca761476 ON public.publics_businessarea USING btree (default_currency_id);


--
-- Name: publics_country_2c7d5721; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX publics_country_2c7d5721 ON public.publics_country USING btree (currency_id);


--
-- Name: publics_country_93469a5b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX publics_country_93469a5b ON public.publics_country USING btree (business_area_id);


--
-- Name: publics_country_vision_code_bb94e64a_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX publics_country_vision_code_bb94e64a_like ON public.publics_country USING btree (vision_code varchar_pattern_ops);


--
-- Name: publics_dsarate_0f442f96; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX publics_dsarate_0f442f96 ON public.publics_dsarate USING btree (region_id);


--
-- Name: publics_dsaregion_93bfec8a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX publics_dsaregion_93bfec8a ON public.publics_dsaregion USING btree (country_id);


--
-- Name: publics_exchangerate_2c7d5721; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX publics_exchangerate_2c7d5721 ON public.publics_exchangerate USING btree (currency_id);


--
-- Name: publics_grant_funds_4e6789a8; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX publics_grant_funds_4e6789a8 ON public.publics_grant_funds USING btree (fund_id);


--
-- Name: publics_grant_funds_c2418e07; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX publics_grant_funds_c2418e07 ON public.publics_grant_funds USING btree (grant_id);


--
-- Name: publics_travelagent_93bfec8a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX publics_travelagent_93bfec8a ON public.publics_travelagent USING btree (country_id);


--
-- Name: publics_wbs_93469a5b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX publics_wbs_93469a5b ON public.publics_wbs USING btree (business_area_id);


--
-- Name: publics_wbs_grants_78655e45; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX publics_wbs_grants_78655e45 ON public.publics_wbs_grants USING btree (wbs_id);


--
-- Name: publics_wbs_grants_c2418e07; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX publics_wbs_grants_c2418e07 ON public.publics_wbs_grants USING btree (grant_id);


--
-- Name: purchase_order_auditorfirm_vendor_number_345a8504_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX purchase_order_auditorfirm_vendor_number_345a8504_like ON public.purchase_order_auditorfirm USING btree (vendor_number varchar_pattern_ops);


--
-- Name: purchase_order_auditorstaffmember_e731b157; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX purchase_order_auditorstaffmember_e731b157 ON public.purchase_order_auditorstaffmember USING btree (auditor_firm_id);


--
-- Name: purchase_order_purchaseorder_e731b157; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX purchase_order_purchaseorder_e731b157 ON public.purchase_order_purchaseorder USING btree (auditor_firm_id);


--
-- Name: purchase_order_purchaseorder_order_number_d1588ef5_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX purchase_order_purchaseorder_order_number_d1588ef5_like ON public.purchase_order_purchaseorder USING btree (order_number varchar_pattern_ops);


--
-- Name: purchase_order_purchaseorderitem_34e01141; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX purchase_order_purchaseorderitem_34e01141 ON public.purchase_order_purchaseorderitem USING btree (purchase_order_id);


--
-- Name: reversion_revision_manager_slug; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX reversion_revision_manager_slug ON public.reversion_revision USING btree (manager_slug);


--
-- Name: reversion_revision_manager_slug_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX reversion_revision_manager_slug_like ON public.reversion_revision USING btree (manager_slug varchar_pattern_ops);


--
-- Name: reversion_revision_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX reversion_revision_user_id ON public.reversion_revision USING btree (user_id);


--
-- Name: reversion_version_content_type_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX reversion_version_content_type_id ON public.reversion_version USING btree (content_type_id);


--
-- Name: reversion_version_object_id_int; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX reversion_version_object_id_int ON public.reversion_version USING btree (object_id_int);


--
-- Name: reversion_version_revision_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX reversion_version_revision_id ON public.reversion_version USING btree (revision_id);


--
-- Name: socialaccount_socialaccount_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX socialaccount_socialaccount_e8701ad4 ON public.socialaccount_socialaccount USING btree (user_id);


--
-- Name: socialaccount_socialapp_sites_9365d6e7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX socialaccount_socialapp_sites_9365d6e7 ON public.socialaccount_socialapp_sites USING btree (site_id);


--
-- Name: socialaccount_socialapp_sites_fe95b0a0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX socialaccount_socialapp_sites_fe95b0a0 ON public.socialaccount_socialapp_sites USING btree (socialapp_id);


--
-- Name: socialaccount_socialtoken_8a089c2a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX socialaccount_socialtoken_8a089c2a ON public.socialaccount_socialtoken USING btree (account_id);


--
-- Name: socialaccount_socialtoken_f382adfe; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX socialaccount_socialtoken_f382adfe ON public.socialaccount_socialtoken USING btree (app_id);


--
-- Name: tpmpartners_tpmpartner_countries_51d7a352; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tpmpartners_tpmpartner_countries_51d7a352 ON public.tpmpartners_tpmpartner_countries USING btree (tpmpartner_id);


--
-- Name: tpmpartners_tpmpartner_countries_93bfec8a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tpmpartners_tpmpartner_countries_93bfec8a ON public.tpmpartners_tpmpartner_countries USING btree (country_id);


--
-- Name: tpmpartners_tpmpartner_vendor_number_7362e934_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tpmpartners_tpmpartner_vendor_number_7362e934_like ON public.tpmpartners_tpmpartner USING btree (vendor_number varchar_pattern_ops);


--
-- Name: tpmpartners_tpmpartnerstaffmember_770dad81; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tpmpartners_tpmpartnerstaffmember_770dad81 ON public.tpmpartners_tpmpartnerstaffmember USING btree (tpm_partner_id);


--
-- Name: unicef_notification_notification_417f1b1c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX unicef_notification_notification_417f1b1c ON public.unicef_notification_notification USING btree (content_type_id);


--
-- Name: unicef_notification_notification_f237b53f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX unicef_notification_notification_f237b53f ON public.unicef_notification_notification USING btree (sent_email_id);


--
-- Name: users_country_0b5fbd3f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_country_0b5fbd3f ON public.users_country USING btree (local_currency_id);


--
-- Name: users_country_domain_url_713208db75d5deb7_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_country_domain_url_713208db75d5deb7_like ON public.users_country USING btree (domain_url varchar_pattern_ops);


--
-- Name: users_country_offices_93bfec8a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_country_offices_93bfec8a ON public.users_country_offices USING btree (country_id);


--
-- Name: users_country_offices_cc247b05; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_country_offices_cc247b05 ON public.users_country_offices USING btree (office_id);


--
-- Name: users_country_schema_name_7ef5cec0a33e4061_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_country_schema_name_7ef5cec0a33e4061_like ON public.users_country USING btree (schema_name varchar_pattern_ops);


--
-- Name: users_office_bd59e407; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_office_bd59e407 ON public.users_office USING btree (zonal_chief_id);


--
-- Name: users_section_code_20a28cc0_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_section_code_20a28cc0_like ON public.users_section USING btree (code varchar_pattern_ops);


--
-- Name: users_section_name_fe821db5f4eb631_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_section_name_fe821db5f4eb631_like ON public.users_section USING btree (name varchar_pattern_ops);


--
-- Name: users_userprofile_8bf76c50; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_userprofile_8bf76c50 ON public.users_userprofile USING btree (oic_id);


--
-- Name: users_userprofile_93bfec8a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_userprofile_93bfec8a ON public.users_userprofile USING btree (country_id);


--
-- Name: users_userprofile_cc247b05; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_userprofile_cc247b05 ON public.users_userprofile USING btree (office_id);


--
-- Name: users_userprofile_countries_available_93bfec8a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_userprofile_countries_available_93bfec8a ON public.users_userprofile_countries_available USING btree (country_id);


--
-- Name: users_userprofile_countries_available_9c2a73e9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_userprofile_countries_available_9c2a73e9 ON public.users_userprofile_countries_available USING btree (userprofile_id);


--
-- Name: users_userprofile_eae0a89e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_userprofile_eae0a89e ON public.users_userprofile USING btree (supervisor_id);


--
-- Name: users_userprofile_f99684b8; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_userprofile_f99684b8 ON public.users_userprofile USING btree (country_override_id);


--
-- Name: users_userprofile_guid_6fab6dc0_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_userprofile_guid_6fab6dc0_like ON public.users_userprofile USING btree (guid varchar_pattern_ops);


--
-- Name: users_userprofile_vendor_number_9a7dcc83_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_userprofile_vendor_number_9a7dcc83_like ON public.users_userprofile USING btree (vendor_number varchar_pattern_ops);


--
-- Name: vision_visionsynclog_93bfec8a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX vision_visionsynclog_93bfec8a ON public.vision_visionsynclog USING btree (country_id);


--
-- Name: waffle_flag_e2fa5388; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX waffle_flag_e2fa5388 ON public.waffle_flag USING btree (created);


--
-- Name: waffle_flag_groups_0e939a4f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX waffle_flag_groups_0e939a4f ON public.waffle_flag_groups USING btree (group_id);


--
-- Name: waffle_flag_groups_6b31b6fd; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX waffle_flag_groups_6b31b6fd ON public.waffle_flag_groups USING btree (flag_id);


--
-- Name: waffle_flag_name_8799ccdf_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX waffle_flag_name_8799ccdf_like ON public.waffle_flag USING btree (name varchar_pattern_ops);


--
-- Name: waffle_flag_users_6b31b6fd; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX waffle_flag_users_6b31b6fd ON public.waffle_flag_users USING btree (flag_id);


--
-- Name: waffle_flag_users_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX waffle_flag_users_e8701ad4 ON public.waffle_flag_users USING btree (user_id);


--
-- Name: waffle_sample_e2fa5388; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX waffle_sample_e2fa5388 ON public.waffle_sample USING btree (created);


--
-- Name: waffle_sample_name_26b507bc_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX waffle_sample_name_26b507bc_like ON public.waffle_sample USING btree (name varchar_pattern_ops);


--
-- Name: waffle_switch_e2fa5388; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX waffle_switch_e2fa5388 ON public.waffle_switch USING btree (created);


--
-- Name: waffle_switch_name_68a12dd8_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX waffle_switch_name_68a12dd8_like ON public.waffle_switch USING btree (name varchar_pattern_ops);


--
-- Name: users_equitrackregistrationmodel D40d9dfb5032f0c5ebdc9f6959e74a4e; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_equitrackregistrationmodel
    ADD CONSTRAINT "D40d9dfb5032f0c5ebdc9f6959e74a4e" FOREIGN KEY (registrationprofile_ptr_id) REFERENCES public.registration_registrationprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_file D78b1919611212d5b020ee49187da39e; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_file
    ADD CONSTRAINT "D78b1919611212d5b020ee49187da39e" FOREIGN KEY (polymorphic_ctype_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: account_emailconfirmation ac_email_address_id_5bcf9f503c32d4d8_fk_account_emailaddress_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT ac_email_address_id_5bcf9f503c32d4d8_fk_account_emailaddress_id FOREIGN KEY (email_address_id) REFERENCES public.account_emailaddress(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: account_emailaddress account_emailaddress_user_id_5c85949e40d9a61d_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_user_id_5c85949e40d9a61d_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_content_type_id_508cf46651277a81_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_content_type_id_508cf46651277a81_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_group_id_689710a9a73b7457_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_group_id_689710a9a73b7457_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user__permission_id_384b62483d7071f0_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user__permission_id_384b62483d7071f0_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permiss_user_id_7f0938558328534a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permiss_user_id_7f0938558328534a_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_celery_beat_periodictask dj_crontab_id_d3cba168_fk_django_celery_beat_crontabschedule_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_periodictask
    ADD CONSTRAINT dj_crontab_id_d3cba168_fk_django_celery_beat_crontabschedule_id FOREIGN KEY (crontab_id) REFERENCES public.django_celery_beat_crontabschedule(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log djan_content_type_id_697914295151027a_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT djan_content_type_id_697914295151027a_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_celery_beat_periodictask django_solar_id_a87ce72c_fk_django_celery_beat_solarschedule_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_periodictask
    ADD CONSTRAINT django_solar_id_a87ce72c_fk_django_celery_beat_solarschedule_id FOREIGN KEY (solar_id) REFERENCES public.django_celery_beat_solarschedule(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djcelery_periodictask djcelery_periodictask_crontab_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.djcelery_periodictask
    ADD CONSTRAINT djcelery_periodictask_crontab_id_fkey FOREIGN KEY (crontab_id) REFERENCES public.djcelery_crontabschedule(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djcelery_periodictask djcelery_periodictask_interval_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.djcelery_periodictask
    ADD CONSTRAINT djcelery_periodictask_interval_id_fkey FOREIGN KEY (interval_id) REFERENCES public.djcelery_intervalschedule(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djcelery_taskstate djcelery_taskstate_worker_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.djcelery_taskstate
    ADD CONSTRAINT djcelery_taskstate_worker_id_fkey FOREIGN KEY (worker_id) REFERENCES public.djcelery_workerstate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: drfpasswordless_callbacktoken drfpasswordless_callbacktoken_user_id_44f30d04_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.drfpasswordless_callbacktoken
    ADD CONSTRAINT drfpasswordless_callbacktoken_user_id_44f30d04_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: easy_thumbnails_thumbnaildimensions e_thumbnail_id_29ad34faceb3c17c_fk_easy_thumbnails_thumbnail_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.easy_thumbnails_thumbnaildimensions
    ADD CONSTRAINT e_thumbnail_id_29ad34faceb3c17c_fk_easy_thumbnails_thumbnail_id FOREIGN KEY (thumbnail_id) REFERENCES public.easy_thumbnails_thumbnail(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: easy_thumbnails_thumbnail easy_thumbnails_thumbnail_source_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.easy_thumbnails_thumbnail
    ADD CONSTRAINT easy_thumbnails_thumbnail_source_id_fkey FOREIGN KEY (source_id) REFERENCES public.easy_thumbnails_source(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: environment_tenantswitch_countries environ_tenantswitch_id_eb4f3277_fk_environment_tenantswitch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantswitch_countries
    ADD CONSTRAINT environ_tenantswitch_id_eb4f3277_fk_environment_tenantswitch_id FOREIGN KEY (tenantswitch_id) REFERENCES public.environment_tenantswitch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: environment_tenantflag_countries environment_tenantflag__country_id_5e04a51c_fk_users_country_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantflag_countries
    ADD CONSTRAINT environment_tenantflag__country_id_5e04a51c_fk_users_country_id FOREIGN KEY (country_id) REFERENCES public.users_country(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: environment_tenantflag_groups environment_tenantflag_group_group_id_062addce_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantflag_groups
    ADD CONSTRAINT environment_tenantflag_group_group_id_062addce_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: environment_tenantflag_groups environment_tenantflag_id_73cc47c1_fk_environment_tenantflag_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantflag_groups
    ADD CONSTRAINT environment_tenantflag_id_73cc47c1_fk_environment_tenantflag_id FOREIGN KEY (tenantflag_id) REFERENCES public.environment_tenantflag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: environment_tenantflag_countries environment_tenantflag_id_77e7b46d_fk_environment_tenantflag_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantflag_countries
    ADD CONSTRAINT environment_tenantflag_id_77e7b46d_fk_environment_tenantflag_id FOREIGN KEY (tenantflag_id) REFERENCES public.environment_tenantflag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: environment_tenantflag_users environment_tenantflag_id_a55b3137_fk_environment_tenantflag_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantflag_users
    ADD CONSTRAINT environment_tenantflag_id_a55b3137_fk_environment_tenantflag_id FOREIGN KEY (tenantflag_id) REFERENCES public.environment_tenantflag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: environment_tenantflag_users environment_tenantflag_users_user_id_e0e51834_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantflag_users
    ADD CONSTRAINT environment_tenantflag_users_user_id_e0e51834_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: environment_tenantswitch_countries environment_tenantswitc_country_id_ec605445_fk_users_country_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_tenantswitch_countries
    ADD CONSTRAINT environment_tenantswitc_country_id_ec605445_fk_users_country_id FOREIGN KEY (country_id) REFERENCES public.users_country(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_clipboarditem filer_clipb_clipboard_id_335d159e1aea2cdc_fk_filer_clipboard_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_clipboarditem
    ADD CONSTRAINT filer_clipb_clipboard_id_335d159e1aea2cdc_fk_filer_clipboard_id FOREIGN KEY (clipboard_id) REFERENCES public.filer_clipboard(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_clipboard filer_clipboard_user_id_2b30c76f2cd235df_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_clipboard
    ADD CONSTRAINT filer_clipboard_user_id_2b30c76f2cd235df_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_clipboarditem filer_clipboarditem_file_id_7b1b6a14b5a3f2b1_fk_filer_file_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_clipboarditem
    ADD CONSTRAINT filer_clipboarditem_file_id_7b1b6a14b5a3f2b1_fk_filer_file_id FOREIGN KEY (file_id) REFERENCES public.filer_file(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_file filer_file_folder_id_24318dda71f59785_fk_filer_folder_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_file
    ADD CONSTRAINT filer_file_folder_id_24318dda71f59785_fk_filer_folder_id FOREIGN KEY (folder_id) REFERENCES public.filer_folder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_file filer_file_owner_id_67317c663ea33283_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_file
    ADD CONSTRAINT filer_file_owner_id_67317c663ea33283_fk_auth_user_id FOREIGN KEY (owner_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_folder filer_folder_owner_id_6527f5f13a76f3ed_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_folder
    ADD CONSTRAINT filer_folder_owner_id_6527f5f13a76f3ed_fk_auth_user_id FOREIGN KEY (owner_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_folder filer_folder_parent_id_4170098ac31c2cbf_fk_filer_folder_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_folder
    ADD CONSTRAINT filer_folder_parent_id_4170098ac31c2cbf_fk_filer_folder_id FOREIGN KEY (parent_id) REFERENCES public.filer_folder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_folderpermission filer_folderpermi_folder_id_442a5347ee209a98_fk_filer_folder_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_folderpermission
    ADD CONSTRAINT filer_folderpermi_folder_id_442a5347ee209a98_fk_filer_folder_id FOREIGN KEY (folder_id) REFERENCES public.filer_folder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_folderpermission filer_folderpermissi_group_id_7c2389ac07ebbde2_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_folderpermission
    ADD CONSTRAINT filer_folderpermissi_group_id_7c2389ac07ebbde2_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_folderpermission filer_folderpermission_user_id_7c6e1a7187a0f15b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_folderpermission
    ADD CONSTRAINT filer_folderpermission_user_id_7c6e1a7187a0f15b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_image filer_image_file_ptr_id_1dde9ad32bce39a6_fk_filer_file_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.filer_image
    ADD CONSTRAINT filer_image_file_ptr_id_1dde9ad32bce39a6_fk_filer_file_id FOREIGN KEY (file_ptr_id) REFERENCES public.filer_file(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_celery_beat_periodictask interval_id_a8ca27da_fk_django_celery_beat_intervalschedule_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_periodictask
    ADD CONSTRAINT interval_id_a8ca27da_fk_django_celery_beat_intervalschedule_id FOREIGN KEY (interval_id) REFERENCES public.django_celery_beat_intervalschedule(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notification_notification notification_content_type_id_fb7eaecb_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_notification
    ADD CONSTRAINT notification_content_type_id_fb7eaecb_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notification_notification notification_not_sent_email_id_660e48c9_fk_post_office_email_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_notification
    ADD CONSTRAINT notification_not_sent_email_id_660e48c9_fk_post_office_email_id FOREIGN KEY (sent_email_id) REFERENCES public.post_office_email(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: purchase_order_purchaseorderitem p_purchase_order_id_50a18f7d_fk_purchase_order_purchaseorder_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order_purchaseorderitem
    ADD CONSTRAINT p_purchase_order_id_50a18f7d_fk_purchase_order_purchaseorder_id FOREIGN KEY (purchase_order_id) REFERENCES public.purchase_order_purchaseorder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: post_office_emailtemplate po_default_template_id_2ac2f889_fk_post_office_emailtemplate_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_office_emailtemplate
    ADD CONSTRAINT po_default_template_id_2ac2f889_fk_post_office_emailtemplate_id FOREIGN KEY (default_template_id) REFERENCES public.post_office_emailtemplate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: post_office_email post_offic_template_id_417da7da_fk_post_office_emailtemplate_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_office_email
    ADD CONSTRAINT post_offic_template_id_417da7da_fk_post_office_emailtemplate_id FOREIGN KEY (template_id) REFERENCES public.post_office_emailtemplate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: post_office_attachment_emails post_office_attachmen_email_id_96875fd9_fk_post_office_email_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_office_attachment_emails
    ADD CONSTRAINT post_office_attachmen_email_id_96875fd9_fk_post_office_email_id FOREIGN KEY (email_id) REFERENCES public.post_office_email(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: post_office_attachment_emails post_office_attachment_id_6136fd9a_fk_post_office_attachment_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_office_attachment_emails
    ADD CONSTRAINT post_office_attachment_id_6136fd9a_fk_post_office_attachment_id FOREIGN KEY (attachment_id) REFERENCES public.post_office_attachment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: post_office_log post_office_log_email_id_d42c8808_fk_post_office_email_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_office_log
    ADD CONSTRAINT post_office_log_email_id_d42c8808_fk_post_office_email_id FOREIGN KEY (email_id) REFERENCES public.post_office_email(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: publics_travelagent public_expense_type_id_e51208b0_fk_publics_travelexpensetype_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_travelagent
    ADD CONSTRAINT public_expense_type_id_e51208b0_fk_publics_travelexpensetype_id FOREIGN KEY (expense_type_id) REFERENCES public.publics_travelexpensetype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: publics_businessarea publics_bus_default_currency_id_be5393fa_fk_publics_currency_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_businessarea
    ADD CONSTRAINT publics_bus_default_currency_id_be5393fa_fk_publics_currency_id FOREIGN KEY (default_currency_id) REFERENCES public.publics_currency(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: publics_businessarea publics_busines_region_id_80fd83c3_fk_publics_businessregion_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_businessarea
    ADD CONSTRAINT publics_busines_region_id_80fd83c3_fk_publics_businessregion_id FOREIGN KEY (region_id) REFERENCES public.publics_businessregion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: publics_country publics_co_business_area_id_fa8bfb5c_fk_publics_businessarea_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_country
    ADD CONSTRAINT publics_co_business_area_id_fa8bfb5c_fk_publics_businessarea_id FOREIGN KEY (business_area_id) REFERENCES public.publics_businessarea(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: publics_country publics_country_currency_id_5850f8d3_fk_publics_currency_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_country
    ADD CONSTRAINT publics_country_currency_id_5850f8d3_fk_publics_currency_id FOREIGN KEY (currency_id) REFERENCES public.publics_currency(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: publics_dsarate publics_dsarate_region_id_cca94016_fk_publics_dsaregion_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_dsarate
    ADD CONSTRAINT publics_dsarate_region_id_cca94016_fk_publics_dsaregion_id FOREIGN KEY (region_id) REFERENCES public.publics_dsaregion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: publics_dsaregion publics_dsaregion_country_id_ca7569f7_fk_publics_country_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_dsaregion
    ADD CONSTRAINT publics_dsaregion_country_id_ca7569f7_fk_publics_country_id FOREIGN KEY (country_id) REFERENCES public.publics_country(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: publics_exchangerate publics_exchangerat_currency_id_4c35406c_fk_publics_currency_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_exchangerate
    ADD CONSTRAINT publics_exchangerat_currency_id_4c35406c_fk_publics_currency_id FOREIGN KEY (currency_id) REFERENCES public.publics_currency(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: publics_grant_funds publics_grant_funds_fund_id_650b7822_fk_publics_fund_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_grant_funds
    ADD CONSTRAINT publics_grant_funds_fund_id_650b7822_fk_publics_fund_id FOREIGN KEY (fund_id) REFERENCES public.publics_fund(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: publics_grant_funds publics_grant_funds_grant_id_4534f58b_fk_publics_grant_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_grant_funds
    ADD CONSTRAINT publics_grant_funds_grant_id_4534f58b_fk_publics_grant_id FOREIGN KEY (grant_id) REFERENCES public.publics_grant(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: publics_travelagent publics_travelagent_country_id_7f8de0ac_fk_publics_country_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_travelagent
    ADD CONSTRAINT publics_travelagent_country_id_7f8de0ac_fk_publics_country_id FOREIGN KEY (country_id) REFERENCES public.publics_country(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: publics_wbs publics_wb_business_area_id_b8f0437f_fk_publics_businessarea_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_wbs
    ADD CONSTRAINT publics_wb_business_area_id_b8f0437f_fk_publics_businessarea_id FOREIGN KEY (business_area_id) REFERENCES public.publics_businessarea(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: publics_wbs_grants publics_wbs_grants_grant_id_2c98a31d_fk_publics_grant_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_wbs_grants
    ADD CONSTRAINT publics_wbs_grants_grant_id_2c98a31d_fk_publics_grant_id FOREIGN KEY (grant_id) REFERENCES public.publics_grant(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: publics_wbs_grants publics_wbs_grants_wbs_id_fca01f48_fk_publics_wbs_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publics_wbs_grants
    ADD CONSTRAINT publics_wbs_grants_wbs_id_fca01f48_fk_publics_wbs_id FOREIGN KEY (wbs_id) REFERENCES public.publics_wbs(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: purchase_order_auditorstaffmember purch_auditor_firm_id_95af9f2f_fk_purchase_order_auditorfirm_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order_auditorstaffmember
    ADD CONSTRAINT purch_auditor_firm_id_95af9f2f_fk_purchase_order_auditorfirm_id FOREIGN KEY (auditor_firm_id) REFERENCES public.purchase_order_auditorfirm(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: purchase_order_purchaseorder purch_auditor_firm_id_ba07a2f9_fk_purchase_order_auditorfirm_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order_purchaseorder
    ADD CONSTRAINT purch_auditor_firm_id_ba07a2f9_fk_purchase_order_auditorfirm_id FOREIGN KEY (auditor_firm_id) REFERENCES public.purchase_order_auditorfirm(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: purchase_order_auditorstaffmember purchase_order_auditorstaffmem_user_id_795ea53d_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order_auditorstaffmember
    ADD CONSTRAINT purchase_order_auditorstaffmem_user_id_795ea53d_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registration_emailregistrationprofile registration_emailregistrationp_registrationprofile_ptr_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registration_emailregistrationprofile
    ADD CONSTRAINT registration_emailregistrationp_registrationprofile_ptr_id_fkey FOREIGN KEY (registrationprofile_ptr_id) REFERENCES public.registration_registrationprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reversion_version reversion_version_revision_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reversion_version
    ADD CONSTRAINT reversion_version_revision_id_fkey FOREIGN KEY (revision_id) REFERENCES public.reversion_revision(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialtoken s_account_id_3fc809e243dd8c0a_fk_socialaccount_socialaccount_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT s_account_id_3fc809e243dd8c0a_fk_socialaccount_socialaccount_id FOREIGN KEY (account_id) REFERENCES public.socialaccount_socialaccount(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialapp_sites soc_socialapp_id_7b02380b6127b1b8_fk_socialaccount_socialapp_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT soc_socialapp_id_7b02380b6127b1b8_fk_socialaccount_socialapp_id FOREIGN KEY (socialapp_id) REFERENCES public.socialaccount_socialapp(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialtoken socialacco_app_id_2125549785bd662_fk_socialaccount_socialapp_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialacco_app_id_2125549785bd662_fk_socialaccount_socialapp_id FOREIGN KEY (app_id) REFERENCES public.socialaccount_socialapp(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialapp_sites socialaccount_sociala_site_id_a859406a22be3fe_fk_django_site_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_sociala_site_id_a859406a22be3fe_fk_django_site_id FOREIGN KEY (site_id) REFERENCES public.django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tpmpartners_tpmpartnerstaffmember tpmpartner_tpm_partner_id_dd932eed_fk_tpmpartners_tpmpartner_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tpmpartners_tpmpartnerstaffmember
    ADD CONSTRAINT tpmpartner_tpm_partner_id_dd932eed_fk_tpmpartners_tpmpartner_id FOREIGN KEY (tpm_partner_id) REFERENCES public.tpmpartners_tpmpartner(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tpmpartners_tpmpartner_countries tpmpartners_tpmpartner__country_id_bbe7ae0a_fk_users_country_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tpmpartners_tpmpartner_countries
    ADD CONSTRAINT tpmpartners_tpmpartner__country_id_bbe7ae0a_fk_users_country_id FOREIGN KEY (country_id) REFERENCES public.users_country(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tpmpartners_tpmpartner_countries tpmpartners_tpmpartner_id_f5f14a1e_fk_tpmpartners_tpmpartner_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tpmpartners_tpmpartner_countries
    ADD CONSTRAINT tpmpartners_tpmpartner_id_f5f14a1e_fk_tpmpartners_tpmpartner_id FOREIGN KEY (tpmpartner_id) REFERENCES public.tpmpartners_tpmpartner(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tpmpartners_tpmpartnerstaffmember tpmpartners_tpmpartnerstaffmem_user_id_1d089bda_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tpmpartners_tpmpartnerstaffmember
    ADD CONSTRAINT tpmpartners_tpmpartnerstaffmem_user_id_1d089bda_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: unicef_notification_notification unicef_notif_content_type_id_4e9cc3f9_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.unicef_notification_notification
    ADD CONSTRAINT unicef_notif_content_type_id_4e9cc3f9_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: unicef_notification_notification unicef_notificat_sent_email_id_399df9cd_fk_post_office_email_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.unicef_notification_notification
    ADD CONSTRAINT unicef_notificat_sent_email_id_399df9cd_fk_post_office_email_id FOREIGN KEY (sent_email_id) REFERENCES public.post_office_email(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_userprofile users__country_override_id_4de609908747de6b_fk_users_country_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users__country_override_id_4de609908747de6b_fk_users_country_id FOREIGN KEY (country_override_id) REFERENCES public.users_country(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_country users_country_local_currency_id_501c1509_fk_publics_currency_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_country
    ADD CONSTRAINT users_country_local_currency_id_501c1509_fk_publics_currency_id FOREIGN KEY (local_currency_id) REFERENCES public.publics_currency(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_country_offices users_country_o_country_id_1e55a08f3bcf03b3_fk_users_country_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_country_offices
    ADD CONSTRAINT users_country_o_country_id_1e55a08f3bcf03b3_fk_users_country_id FOREIGN KEY (country_id) REFERENCES public.users_country(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_country_offices users_country_off_office_id_52ebc125913460cc_fk_users_office_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_country_offices
    ADD CONSTRAINT users_country_off_office_id_52ebc125913460cc_fk_users_office_id FOREIGN KEY (office_id) REFERENCES public.users_office(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_office users_office_zonal_chief_id_2f404077b36e0282_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_office
    ADD CONSTRAINT users_office_zonal_chief_id_2f404077b36e0282_fk_auth_user_id FOREIGN KEY (zonal_chief_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_userprofile_countries_available users_u_userprofile_id_35fe3e2d262bf6c6_fk_users_userprofile_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_userprofile_countries_available
    ADD CONSTRAINT users_u_userprofile_id_35fe3e2d262bf6c6_fk_users_userprofile_id FOREIGN KEY (userprofile_id) REFERENCES public.users_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_userprofile_countries_available users_userprofi_country_id_1ce0e19bda636668_fk_users_country_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_userprofile_countries_available
    ADD CONSTRAINT users_userprofi_country_id_1ce0e19bda636668_fk_users_country_id FOREIGN KEY (country_id) REFERENCES public.users_country(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_userprofile users_userprofi_country_id_2357c4275868743b_fk_users_country_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofi_country_id_2357c4275868743b_fk_users_country_id FOREIGN KEY (country_id) REFERENCES public.users_country(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_userprofile users_userprofile_office_id_7b50fef57c0f044_fk_users_office_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofile_office_id_7b50fef57c0f044_fk_users_office_id FOREIGN KEY (office_id) REFERENCES public.users_office(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_userprofile users_userprofile_oic_id_3ee801a8_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofile_oic_id_3ee801a8_fk_auth_user_id FOREIGN KEY (oic_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_userprofile users_userprofile_supervisor_id_2ff458c6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofile_supervisor_id_2ff458c6_fk_auth_user_id FOREIGN KEY (supervisor_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_workspacecounter users_workspacecounte_workspace_id_1e710472_fk_users_country_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_workspacecounter
    ADD CONSTRAINT users_workspacecounte_workspace_id_1e710472_fk_users_country_id FOREIGN KEY (workspace_id) REFERENCES public.users_country(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: vision_visionsynclog vision_visionsy_country_id_33d90378f535050f_fk_users_country_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vision_visionsynclog
    ADD CONSTRAINT vision_visionsy_country_id_33d90378f535050f_fk_users_country_id FOREIGN KEY (country_id) REFERENCES public.users_country(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: waffle_flag_groups waffle_flag_groups_flag_id_c11c0c05_fk_waffle_flag_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.waffle_flag_groups
    ADD CONSTRAINT waffle_flag_groups_flag_id_c11c0c05_fk_waffle_flag_id FOREIGN KEY (flag_id) REFERENCES public.waffle_flag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: waffle_flag_groups waffle_flag_groups_group_id_a97c4f66_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.waffle_flag_groups
    ADD CONSTRAINT waffle_flag_groups_group_id_a97c4f66_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: waffle_flag_users waffle_flag_users_flag_id_833c37b0_fk_waffle_flag_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.waffle_flag_users
    ADD CONSTRAINT waffle_flag_users_flag_id_833c37b0_fk_waffle_flag_id FOREIGN KEY (flag_id) REFERENCES public.waffle_flag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: waffle_flag_users waffle_flag_users_user_id_8026df9b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.waffle_flag_users
    ADD CONSTRAINT waffle_flag_users_user_id_8026df9b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

