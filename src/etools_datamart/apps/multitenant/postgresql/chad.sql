--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.13
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

--
-- Name: chad; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA chad;


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: action_points_actionpoint; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.action_points_actionpoint (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    status character varying(10) NOT NULL,
    description text NOT NULL,
    due_date date,
    date_of_completion timestamp with time zone,
    assigned_by_id integer NOT NULL,
    assigned_to_id integer NOT NULL,
    author_id integer NOT NULL,
    cp_output_id integer,
    engagement_id integer,
    intervention_id integer,
    location_id integer,
    office_id integer,
    partner_id integer,
    section_id integer,
    tpm_activity_id integer,
    high_priority boolean NOT NULL,
    travel_activity_id integer,
    category_id integer
);


--
-- Name: action_points_actionpoint_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.action_points_actionpoint_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: action_points_actionpoint_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.action_points_actionpoint_id_seq OWNED BY chad.action_points_actionpoint.id;


--
-- Name: activities_activity; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.activities_activity (
    id integer NOT NULL,
    date date,
    cp_output_id integer,
    intervention_id integer,
    partner_id integer
);


--
-- Name: activities_activity_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.activities_activity_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: activities_activity_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.activities_activity_id_seq OWNED BY chad.activities_activity.id;


--
-- Name: activities_activity_locations; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.activities_activity_locations (
    id integer NOT NULL,
    activity_id integer NOT NULL,
    location_id integer NOT NULL
);


--
-- Name: activities_activity_locations_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.activities_activity_locations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: activities_activity_locations_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.activities_activity_locations_id_seq OWNED BY chad.activities_activity_locations.id;


--
-- Name: actstream_action; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.actstream_action (
    id integer NOT NULL,
    actor_object_id character varying(255) NOT NULL,
    verb character varying(255) NOT NULL,
    description text,
    target_object_id character varying(255),
    action_object_object_id character varying(255),
    "timestamp" timestamp with time zone NOT NULL,
    public boolean NOT NULL,
    data text,
    action_object_content_type_id integer,
    actor_content_type_id integer NOT NULL,
    target_content_type_id integer
);


--
-- Name: actstream_action_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.actstream_action_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: actstream_action_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.actstream_action_id_seq OWNED BY chad.actstream_action.id;


--
-- Name: actstream_follow; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.actstream_follow (
    id integer NOT NULL,
    object_id character varying(255) NOT NULL,
    actor_only boolean NOT NULL,
    started timestamp with time zone NOT NULL,
    content_type_id integer NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: actstream_follow_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.actstream_follow_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: actstream_follow_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.actstream_follow_id_seq OWNED BY chad.actstream_follow.id;


--
-- Name: attachments_attachment; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.attachments_attachment (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    file character varying(1024),
    hyperlink character varying(255) NOT NULL,
    object_id integer,
    code character varying(64) NOT NULL,
    content_type_id integer,
    file_type_id integer,
    uploaded_by_id integer
);


--
-- Name: attachments_attachment_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.attachments_attachment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: attachments_attachment_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.attachments_attachment_id_seq OWNED BY chad.attachments_attachment.id;


--
-- Name: attachments_attachmentflat; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.attachments_attachmentflat (
    id integer NOT NULL,
    partner character varying(255) NOT NULL,
    partner_type character varying(150) NOT NULL,
    vendor_number character varying(50) NOT NULL,
    pd_ssfa_number character varying(64) NOT NULL,
    file_type character varying(100) NOT NULL,
    file_link character varying(1024) NOT NULL,
    uploaded_by character varying(255) NOT NULL,
    created character varying(50) NOT NULL,
    attachment_id integer NOT NULL,
    filename character varying(1024) NOT NULL,
    agreement_reference_number character varying(100) NOT NULL,
    object_link character varying(200) NOT NULL
);


--
-- Name: attachments_attachmentflat_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.attachments_attachmentflat_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: attachments_attachmentflat_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.attachments_attachmentflat_id_seq OWNED BY chad.attachments_attachmentflat.id;


--
-- Name: attachments_filetype; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.attachments_filetype (
    id integer NOT NULL,
    "order" integer NOT NULL,
    name character varying(64) NOT NULL,
    code character varying(64) NOT NULL,
    label character varying(64) NOT NULL,
    CONSTRAINT attachments_filetype_order_check CHECK (("order" >= 0))
);


--
-- Name: attachments_filetype_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.attachments_filetype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: attachments_filetype_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.attachments_filetype_id_seq OWNED BY chad.attachments_filetype.id;


--
-- Name: audit_audit; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.audit_audit (
    engagement_ptr_id integer NOT NULL,
    audited_expenditure numeric(20,2),
    financial_findings numeric(20,2),
    audit_opinion character varying(20) NOT NULL
);


--
-- Name: audit_detailedfindinginfo; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.audit_detailedfindinginfo (
    id integer NOT NULL,
    finding text NOT NULL,
    recommendation text NOT NULL,
    micro_assesment_id integer NOT NULL
);


--
-- Name: audit_detailedfindinginfo_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.audit_detailedfindinginfo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: audit_detailedfindinginfo_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.audit_detailedfindinginfo_id_seq OWNED BY chad.audit_detailedfindinginfo.id;


--
-- Name: audit_engagement; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.audit_engagement (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    status character varying(30) NOT NULL,
    partner_contacted_at date,
    engagement_type character varying(10) NOT NULL,
    start_date date,
    end_date date,
    total_value numeric(20,2),
    date_of_field_visit date,
    date_of_draft_report_to_ip date,
    date_of_comments_by_ip date,
    date_of_draft_report_to_unicef date,
    date_of_comments_by_unicef date,
    date_of_report_submit date,
    date_of_final_report date,
    date_of_cancel date,
    amount_refunded numeric(20,2),
    additional_supporting_documentation_provided numeric(20,2),
    justification_provided_and_accepted numeric(20,2),
    write_off_required numeric(20,2),
    cancel_comment text NOT NULL,
    explanation_for_additional_information text NOT NULL,
    partner_id integer NOT NULL,
    joint_audit boolean NOT NULL,
    agreement_id integer NOT NULL,
    po_item_id integer,
    shared_ip_with character varying(20)[] NOT NULL,
    exchange_rate numeric(20,2)
);


--
-- Name: audit_engagement_active_pd; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.audit_engagement_active_pd (
    id integer NOT NULL,
    engagement_id integer NOT NULL,
    intervention_id integer NOT NULL
);


--
-- Name: audit_engagement_active_pd_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.audit_engagement_active_pd_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: audit_engagement_active_pd_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.audit_engagement_active_pd_id_seq OWNED BY chad.audit_engagement_active_pd.id;


--
-- Name: audit_engagement_authorized_officers; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.audit_engagement_authorized_officers (
    id integer NOT NULL,
    engagement_id integer NOT NULL,
    partnerstaffmember_id integer NOT NULL
);


--
-- Name: audit_engagement_authorized_officers_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.audit_engagement_authorized_officers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: audit_engagement_authorized_officers_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.audit_engagement_authorized_officers_id_seq OWNED BY chad.audit_engagement_authorized_officers.id;


--
-- Name: audit_engagement_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.audit_engagement_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: audit_engagement_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.audit_engagement_id_seq OWNED BY chad.audit_engagement.id;


--
-- Name: audit_engagement_staff_members; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.audit_engagement_staff_members (
    id integer NOT NULL,
    engagement_id integer NOT NULL,
    auditorstaffmember_id integer NOT NULL
);


--
-- Name: audit_engagement_staff_members1_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.audit_engagement_staff_members1_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: audit_engagement_staff_members1_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.audit_engagement_staff_members1_id_seq OWNED BY chad.audit_engagement_staff_members.id;


--
-- Name: audit_financialfinding; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.audit_financialfinding (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    local_amount numeric(20,2) NOT NULL,
    amount numeric(20,2) NOT NULL,
    description text NOT NULL,
    recommendation text NOT NULL,
    ip_comments text NOT NULL,
    audit_id integer NOT NULL
);


--
-- Name: audit_financialfinding_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.audit_financialfinding_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: audit_financialfinding_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.audit_financialfinding_id_seq OWNED BY chad.audit_financialfinding.id;


--
-- Name: audit_finding; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.audit_finding (
    id integer NOT NULL,
    priority character varying(4) NOT NULL,
    category_of_observation character varying(100) NOT NULL,
    recommendation text NOT NULL,
    agreed_action_by_ip text NOT NULL,
    deadline_of_action date,
    spot_check_id integer NOT NULL
);


--
-- Name: audit_finding_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.audit_finding_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: audit_finding_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.audit_finding_id_seq OWNED BY chad.audit_finding.id;


--
-- Name: audit_keyinternalcontrol; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.audit_keyinternalcontrol (
    id integer NOT NULL,
    recommendation text NOT NULL,
    audit_observation text NOT NULL,
    ip_response text NOT NULL,
    audit_id integer NOT NULL
);


--
-- Name: audit_keyinternalcontrol_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.audit_keyinternalcontrol_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: audit_keyinternalcontrol_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.audit_keyinternalcontrol_id_seq OWNED BY chad.audit_keyinternalcontrol.id;


--
-- Name: audit_microassessment; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.audit_microassessment (
    engagement_ptr_id integer NOT NULL
);


--
-- Name: audit_risk; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.audit_risk (
    id integer NOT NULL,
    value smallint,
    extra jsonb,
    blueprint_id integer NOT NULL,
    engagement_id integer NOT NULL
);


--
-- Name: audit_risk_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.audit_risk_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: audit_risk_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.audit_risk_id_seq OWNED BY chad.audit_risk.id;


--
-- Name: audit_riskblueprint; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.audit_riskblueprint (
    id integer NOT NULL,
    "order" integer NOT NULL,
    weight smallint NOT NULL,
    is_key boolean NOT NULL,
    header text NOT NULL,
    description text NOT NULL,
    category_id integer NOT NULL,
    CONSTRAINT audit_riskblueprint_order_check CHECK (("order" >= 0)),
    CONSTRAINT audit_riskblueprint_weight_check CHECK ((weight >= 0))
);


--
-- Name: audit_riskblueprint_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.audit_riskblueprint_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: audit_riskblueprint_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.audit_riskblueprint_id_seq OWNED BY chad.audit_riskblueprint.id;


--
-- Name: audit_riskcategory; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.audit_riskcategory (
    id integer NOT NULL,
    "order" integer NOT NULL,
    header character varying(255) NOT NULL,
    category_type character varying(20) NOT NULL,
    code character varying(20) NOT NULL,
    parent_id integer,
    CONSTRAINT audit_riskcategory_order_check CHECK (("order" >= 0))
);


--
-- Name: audit_riskcategory_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.audit_riskcategory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: audit_riskcategory_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.audit_riskcategory_id_seq OWNED BY chad.audit_riskcategory.id;


--
-- Name: audit_specialaudit; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.audit_specialaudit (
    engagement_ptr_id integer NOT NULL
);


--
-- Name: audit_specialauditrecommendation; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.audit_specialauditrecommendation (
    id integer NOT NULL,
    description text NOT NULL,
    audit_id integer NOT NULL
);


--
-- Name: audit_specialauditrecommendation_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.audit_specialauditrecommendation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: audit_specialauditrecommendation_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.audit_specialauditrecommendation_id_seq OWNED BY chad.audit_specialauditrecommendation.id;


--
-- Name: audit_specificprocedure; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.audit_specificprocedure (
    id integer NOT NULL,
    description text NOT NULL,
    finding text NOT NULL,
    audit_id integer NOT NULL
);


--
-- Name: audit_specificprocedure_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.audit_specificprocedure_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: audit_specificprocedure_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.audit_specificprocedure_id_seq OWNED BY chad.audit_specificprocedure.id;


--
-- Name: audit_spotcheck; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.audit_spotcheck (
    engagement_ptr_id integer NOT NULL,
    total_amount_tested numeric(20,2),
    total_amount_of_ineligible_expenditure numeric(20,2),
    internal_controls text NOT NULL
);


--
-- Name: django_comment_flags; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.django_comment_flags (
    id integer NOT NULL,
    flag character varying(30) NOT NULL,
    flag_date timestamp with time zone NOT NULL,
    comment_id integer NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: django_comment_flags_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.django_comment_flags_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_comment_flags_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.django_comment_flags_id_seq OWNED BY chad.django_comment_flags.id;


--
-- Name: django_comments; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.django_comments (
    id integer NOT NULL,
    object_pk text NOT NULL,
    user_name character varying(50) NOT NULL,
    user_email character varying(254) NOT NULL,
    user_url character varying(200) NOT NULL,
    comment text NOT NULL,
    submit_date timestamp with time zone NOT NULL,
    ip_address inet,
    is_public boolean NOT NULL,
    is_removed boolean NOT NULL,
    content_type_id integer NOT NULL,
    site_id integer NOT NULL,
    user_id integer
);


--
-- Name: django_comments_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.django_comments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_comments_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.django_comments_id_seq OWNED BY chad.django_comments.id;


--
-- Name: django_migrations; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.django_migrations_id_seq OWNED BY chad.django_migrations.id;


--
-- Name: funds_donor; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.funds_donor (
    id integer NOT NULL,
    name character varying(45) NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL
);


--
-- Name: funds_donor_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.funds_donor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: funds_donor_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.funds_donor_id_seq OWNED BY chad.funds_donor.id;


--
-- Name: funds_fundscommitmentheader; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.funds_fundscommitmentheader (
    id integer NOT NULL,
    vendor_code character varying(20) NOT NULL,
    fc_number character varying(20) NOT NULL,
    document_date date,
    fc_type character varying(50) NOT NULL,
    currency character varying(50) NOT NULL,
    document_text character varying(255) NOT NULL,
    exchange_rate character varying(20) NOT NULL,
    responsible_person character varying(100),
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL
);


--
-- Name: funds_fundscommitmentheader_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.funds_fundscommitmentheader_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: funds_fundscommitmentheader_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.funds_fundscommitmentheader_id_seq OWNED BY chad.funds_fundscommitmentheader.id;


--
-- Name: funds_fundscommitmentitem; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.funds_fundscommitmentitem (
    id integer NOT NULL,
    fc_ref_number character varying(30) NOT NULL,
    line_item character varying(5) NOT NULL,
    wbs character varying(30) NOT NULL,
    grant_number character varying(20) NOT NULL,
    fund character varying(10) NOT NULL,
    gl_account character varying(15) NOT NULL,
    due_date date,
    fr_number character varying(20) NOT NULL,
    commitment_amount numeric(20,2) NOT NULL,
    commitment_amount_dc numeric(20,2) NOT NULL,
    amount_changed numeric(20,2) NOT NULL,
    line_item_text character varying(255) NOT NULL,
    fund_commitment_id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL
);


--
-- Name: funds_fundscommitmentitem_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.funds_fundscommitmentitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: funds_fundscommitmentitem_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.funds_fundscommitmentitem_id_seq OWNED BY chad.funds_fundscommitmentitem.id;


--
-- Name: funds_fundsreservationheader; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.funds_fundsreservationheader (
    id integer NOT NULL,
    vendor_code character varying(20) NOT NULL,
    fr_number character varying(20) NOT NULL,
    document_date date,
    fr_type character varying(50) NOT NULL,
    currency character varying(50) NOT NULL,
    document_text character varying(255) NOT NULL,
    start_date date,
    end_date date,
    actual_amt numeric(20,2) NOT NULL,
    intervention_id integer,
    intervention_amt numeric(20,2) NOT NULL,
    outstanding_amt numeric(20,2) NOT NULL,
    total_amt numeric(20,2) NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    actual_amt_local numeric(20,2) NOT NULL,
    outstanding_amt_local numeric(20,2) NOT NULL,
    total_amt_local numeric(20,2) NOT NULL,
    multi_curr_flag boolean NOT NULL
);


--
-- Name: funds_fundsreservationheader_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.funds_fundsreservationheader_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: funds_fundsreservationheader_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.funds_fundsreservationheader_id_seq OWNED BY chad.funds_fundsreservationheader.id;


--
-- Name: funds_fundsreservationitem; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.funds_fundsreservationitem (
    id integer NOT NULL,
    fr_ref_number character varying(30) NOT NULL,
    line_item smallint NOT NULL,
    wbs character varying(30) NOT NULL,
    grant_number character varying(20) NOT NULL,
    fund character varying(10) NOT NULL,
    overall_amount numeric(20,2) NOT NULL,
    overall_amount_dc numeric(20,2) NOT NULL,
    due_date date,
    line_item_text character varying(255) NOT NULL,
    fund_reservation_id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    donor character varying(256),
    donor_code character varying(30),
    CONSTRAINT funds_fundsreservationitem_line_item_a0d89637_check CHECK ((line_item >= 0))
);


--
-- Name: funds_fundsreservationitem_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.funds_fundsreservationitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: funds_fundsreservationitem_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.funds_fundsreservationitem_id_seq OWNED BY chad.funds_fundsreservationitem.id;


--
-- Name: funds_grant; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.funds_grant (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    description character varying(255) NOT NULL,
    expiry date,
    donor_id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL
);


--
-- Name: funds_grant_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.funds_grant_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: funds_grant_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.funds_grant_id_seq OWNED BY chad.funds_grant.id;


--
-- Name: hact_aggregatehact; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.hact_aggregatehact (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    year integer NOT NULL,
    partner_values jsonb
);


--
-- Name: hact_aggregatehact_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.hact_aggregatehact_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: hact_aggregatehact_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.hact_aggregatehact_id_seq OWNED BY chad.hact_aggregatehact.id;


--
-- Name: hact_hacthistory; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.hact_hacthistory (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    year integer NOT NULL,
    partner_values jsonb,
    partner_id integer NOT NULL
);


--
-- Name: hact_hacthistory_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.hact_hacthistory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: hact_hacthistory_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.hact_hacthistory_id_seq OWNED BY chad.hact_hacthistory.id;


--
-- Name: locations_cartodbtable; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.locations_cartodbtable (
    id integer NOT NULL,
    domain character varying(254) NOT NULL,
    api_key character varying(254) NOT NULL,
    table_name character varying(254) NOT NULL,
    display_name character varying(254) NOT NULL,
    name_col character varying(254) NOT NULL,
    pcode_col character varying(254) NOT NULL,
    parent_code_col character varying(254) NOT NULL,
    color character varying(7) NOT NULL,
    lft integer NOT NULL,
    rght integer NOT NULL,
    tree_id integer NOT NULL,
    level integer NOT NULL,
    location_type_id integer NOT NULL,
    parent_id integer,
    CONSTRAINT locations_cartodbtable_level_check CHECK ((level >= 0)),
    CONSTRAINT locations_cartodbtable_lft_check CHECK ((lft >= 0)),
    CONSTRAINT locations_cartodbtable_rght_check CHECK ((rght >= 0)),
    CONSTRAINT locations_cartodbtable_tree_id_check CHECK ((tree_id >= 0))
);


--
-- Name: locations_cartodbtable_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.locations_cartodbtable_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: locations_cartodbtable_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.locations_cartodbtable_id_seq OWNED BY chad.locations_cartodbtable.id;


--
-- Name: locations_gatewaytype; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.locations_gatewaytype (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    admin_level smallint,
    CONSTRAINT locations_gatewaytype_admin_level_check CHECK ((admin_level >= 0))
);


--
-- Name: locations_gatewaytype_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.locations_gatewaytype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: locations_gatewaytype_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.locations_gatewaytype_id_seq OWNED BY chad.locations_gatewaytype.id;


--
-- Name: locations_location; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.locations_location (
    id integer NOT NULL,
    name character varying(254) NOT NULL,
    latitude double precision,
    longitude double precision,
    p_code character varying(32) NOT NULL,
    geom public.geometry(MultiPolygon,4326),
    point public.geometry(Point,4326),
    lft integer NOT NULL,
    rght integer NOT NULL,
    tree_id integer NOT NULL,
    level integer NOT NULL,
    gateway_id integer NOT NULL,
    parent_id integer,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    CONSTRAINT locations_location_level_check CHECK ((level >= 0)),
    CONSTRAINT locations_location_lft_check CHECK ((lft >= 0)),
    CONSTRAINT locations_location_rght_check CHECK ((rght >= 0)),
    CONSTRAINT locations_location_tree_id_check CHECK ((tree_id >= 0))
);


--
-- Name: locations_location_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.locations_location_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: locations_location_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.locations_location_id_seq OWNED BY chad.locations_location.id;


--
-- Name: management_flaggedissue; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.management_flaggedissue (
    id integer NOT NULL,
    object_id integer NOT NULL,
    date_created timestamp with time zone NOT NULL,
    date_updated timestamp with time zone NOT NULL,
    issue_category character varying(32) NOT NULL,
    issue_id character varying(100) NOT NULL,
    message text NOT NULL,
    content_type_id integer NOT NULL,
    issue_status character varying(32) NOT NULL,
    CONSTRAINT management_flaggedissue_object_id_check CHECK ((object_id >= 0))
);


--
-- Name: management_flaggedissue_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.management_flaggedissue_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: management_flaggedissue_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.management_flaggedissue_id_seq OWNED BY chad.management_flaggedissue.id;


--
-- Name: partners_agreement; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_agreement (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    agreement_type character varying(10) NOT NULL,
    agreement_number character varying(45) NOT NULL,
    attached_agreement character varying(1024) NOT NULL,
    start date,
    "end" date,
    signed_by_unicef_date date,
    signed_by_partner_date date,
    partner_id integer NOT NULL,
    partner_manager_id integer,
    signed_by_id integer,
    status character varying(32) NOT NULL,
    country_programme_id integer,
    reference_number_year integer NOT NULL,
    special_conditions_pca boolean NOT NULL
);


--
-- Name: partners_agreement_authorized_officers; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_agreement_authorized_officers (
    id integer NOT NULL,
    agreement_id integer NOT NULL,
    partnerstaffmember_id integer NOT NULL
);


--
-- Name: partners_agreement_authorized_officers_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_agreement_authorized_officers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_agreement_authorized_officers_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_agreement_authorized_officers_id_seq OWNED BY chad.partners_agreement_authorized_officers.id;


--
-- Name: partners_agreement_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_agreement_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_agreement_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_agreement_id_seq OWNED BY chad.partners_agreement.id;


--
-- Name: partners_agreementamendment; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_agreementamendment (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    number character varying(5) NOT NULL,
    signed_amendment character varying(1024),
    signed_date date,
    agreement_id integer NOT NULL,
    types character varying(50)[] NOT NULL
);


--
-- Name: partners_agreementamendment_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_agreementamendment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_agreementamendment_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_agreementamendment_id_seq OWNED BY chad.partners_agreementamendment.id;


--
-- Name: partners_assessment; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_assessment (
    id integer NOT NULL,
    type character varying(50) NOT NULL,
    names_of_other_agencies character varying(255),
    expected_budget integer,
    notes character varying(255),
    requested_date date NOT NULL,
    planned_date date,
    completed_date date,
    rating character varying(50) NOT NULL,
    report character varying(1024),
    current boolean NOT NULL,
    approving_officer_id integer,
    partner_id integer NOT NULL,
    requesting_officer_id integer,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL
);


--
-- Name: partners_assessment_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_assessment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_assessment_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_assessment_id_seq OWNED BY chad.partners_assessment.id;


--
-- Name: partners_corevaluesassessment; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_corevaluesassessment (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    date date,
    assessment character varying(1024),
    archived boolean NOT NULL,
    partner_id integer NOT NULL
);


--
-- Name: partners_corevaluesassessment_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_corevaluesassessment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_corevaluesassessment_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_corevaluesassessment_id_seq OWNED BY chad.partners_corevaluesassessment.id;


--
-- Name: partners_directcashtransfer; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_directcashtransfer (
    id integer NOT NULL,
    fc_ref character varying(50) NOT NULL,
    amount_usd numeric(20,2) NOT NULL,
    liquidation_usd numeric(20,2) NOT NULL,
    outstanding_balance_usd numeric(20,2) NOT NULL,
    "amount_less_than_3_Months_usd" numeric(20,2) NOT NULL,
    amount_3_to_6_months_usd numeric(20,2) NOT NULL,
    amount_6_to_9_months_usd numeric(20,2) NOT NULL,
    "amount_more_than_9_Months_usd" numeric(20,2) NOT NULL
);


--
-- Name: partners_directcashtransfer_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_directcashtransfer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_directcashtransfer_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_directcashtransfer_id_seq OWNED BY chad.partners_directcashtransfer.id;


--
-- Name: partners_filetype; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_filetype (
    id integer NOT NULL,
    name character varying(64) NOT NULL
);


--
-- Name: partners_filetype_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_filetype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_filetype_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_filetype_id_seq OWNED BY chad.partners_filetype.id;


--
-- Name: partners_fundingcommitment; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_fundingcommitment (
    id integer NOT NULL,
    start timestamp with time zone,
    "end" timestamp with time zone,
    fr_number character varying(50) NOT NULL,
    wbs character varying(50) NOT NULL,
    fc_type character varying(50) NOT NULL,
    fc_ref character varying(50),
    fr_item_amount_usd numeric(20,2),
    agreement_amount numeric(20,2),
    commitment_amount numeric(20,2),
    expenditure_amount numeric(20,2),
    grant_id integer
);


--
-- Name: partners_fundingcommitment_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_fundingcommitment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_fundingcommitment_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_fundingcommitment_id_seq OWNED BY chad.partners_fundingcommitment.id;


--
-- Name: partners_intervention; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_intervention (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    document_type character varying(255) NOT NULL,
    number character varying(64),
    title character varying(256) NOT NULL,
    status character varying(32) NOT NULL,
    start date,
    "end" date,
    submission_date date,
    submission_date_prc date,
    review_date_prc date,
    prc_review_document character varying(1024),
    signed_by_unicef_date date,
    signed_by_partner_date date,
    population_focus character varying(130),
    agreement_id integer NOT NULL,
    partner_authorized_officer_signatory_id integer,
    unicef_signatory_id integer,
    signed_pd_document character varying(1024),
    country_programme_id integer,
    contingency_pd boolean NOT NULL,
    metadata jsonb,
    in_amendment boolean NOT NULL,
    reference_number_year integer,
    signed_by_unicef boolean NOT NULL
);


--
-- Name: partners_intervention_flat_locations; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_intervention_flat_locations (
    id integer NOT NULL,
    intervention_id integer NOT NULL,
    location_id integer NOT NULL
);


--
-- Name: partners_intervention_flat_locations_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_intervention_flat_locations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_intervention_flat_locations_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_intervention_flat_locations_id_seq OWNED BY chad.partners_intervention_flat_locations.id;


--
-- Name: partners_intervention_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_intervention_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_intervention_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_intervention_id_seq OWNED BY chad.partners_intervention.id;


--
-- Name: partners_intervention_offices; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_intervention_offices (
    id integer NOT NULL,
    intervention_id integer NOT NULL,
    office_id integer NOT NULL
);


--
-- Name: partners_intervention_offices_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_intervention_offices_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_intervention_offices_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_intervention_offices_id_seq OWNED BY chad.partners_intervention_offices.id;


--
-- Name: partners_intervention_partner_focal_points; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_intervention_partner_focal_points (
    id integer NOT NULL,
    intervention_id integer NOT NULL,
    partnerstaffmember_id integer NOT NULL
);


--
-- Name: partners_intervention_partner_focal_points_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_intervention_partner_focal_points_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_intervention_partner_focal_points_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_intervention_partner_focal_points_id_seq OWNED BY chad.partners_intervention_partner_focal_points.id;


--
-- Name: partners_intervention_sections; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_intervention_sections (
    id integer NOT NULL,
    intervention_id integer NOT NULL,
    sector_id integer NOT NULL
);


--
-- Name: partners_intervention_sections_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_intervention_sections_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_intervention_sections_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_intervention_sections_id_seq OWNED BY chad.partners_intervention_sections.id;


--
-- Name: partners_intervention_unicef_focal_points; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_intervention_unicef_focal_points (
    id integer NOT NULL,
    intervention_id integer NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: partners_intervention_unicef_focal_points_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_intervention_unicef_focal_points_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_intervention_unicef_focal_points_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_intervention_unicef_focal_points_id_seq OWNED BY chad.partners_intervention_unicef_focal_points.id;


--
-- Name: partners_interventionamendment; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_interventionamendment (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    signed_date date,
    amendment_number integer NOT NULL,
    signed_amendment character varying(1024) NOT NULL,
    intervention_id integer NOT NULL,
    types character varying(50)[] NOT NULL,
    other_description character varying(512)
);


--
-- Name: partners_interventionamendment_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_interventionamendment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_interventionamendment_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_interventionamendment_id_seq OWNED BY chad.partners_interventionamendment.id;


--
-- Name: partners_interventionattachment; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_interventionattachment (
    id integer NOT NULL,
    attachment character varying(1024) NOT NULL,
    intervention_id integer NOT NULL,
    type_id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL
);


--
-- Name: partners_interventionattachment_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_interventionattachment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_interventionattachment_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_interventionattachment_id_seq OWNED BY chad.partners_interventionattachment.id;


--
-- Name: partners_interventionbudget; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_interventionbudget (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    partner_contribution numeric(20,2) NOT NULL,
    unicef_cash numeric(20,2) NOT NULL,
    in_kind_amount numeric(20,2) NOT NULL,
    partner_contribution_local numeric(20,2) NOT NULL,
    unicef_cash_local numeric(20,2) NOT NULL,
    in_kind_amount_local numeric(20,2) NOT NULL,
    total numeric(20,2) NOT NULL,
    intervention_id integer,
    total_local numeric(20,2) NOT NULL,
    currency character varying(4) NOT NULL
);


--
-- Name: partners_interventionbudget_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_interventionbudget_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_interventionbudget_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_interventionbudget_id_seq OWNED BY chad.partners_interventionbudget.id;


--
-- Name: partners_interventionplannedvisits; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_interventionplannedvisits (
    id integer NOT NULL,
    year integer NOT NULL,
    programmatic_q4 integer NOT NULL,
    intervention_id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    programmatic_q1 integer NOT NULL,
    programmatic_q2 integer NOT NULL,
    programmatic_q3 integer NOT NULL
);


--
-- Name: partners_interventionplannedvisits_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_interventionplannedvisits_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_interventionplannedvisits_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_interventionplannedvisits_id_seq OWNED BY chad.partners_interventionplannedvisits.id;


--
-- Name: partners_interventionreportingperiod; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_interventionreportingperiod (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    due_date date NOT NULL,
    intervention_id integer NOT NULL
);


--
-- Name: partners_interventionreportingperiod_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_interventionreportingperiod_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_interventionreportingperiod_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_interventionreportingperiod_id_seq OWNED BY chad.partners_interventionreportingperiod.id;


--
-- Name: partners_interventionresultlink; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_interventionresultlink (
    id integer NOT NULL,
    cp_output_id integer NOT NULL,
    intervention_id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL
);


--
-- Name: partners_interventionresultlink_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_interventionresultlink_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_interventionresultlink_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_interventionresultlink_id_seq OWNED BY chad.partners_interventionresultlink.id;


--
-- Name: partners_interventionresultlink_ram_indicators; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_interventionresultlink_ram_indicators (
    id integer NOT NULL,
    interventionresultlink_id integer NOT NULL,
    indicator_id integer NOT NULL
);


--
-- Name: partners_interventionresultlink_ram_indicators_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_interventionresultlink_ram_indicators_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_interventionresultlink_ram_indicators_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_interventionresultlink_ram_indicators_id_seq OWNED BY chad.partners_interventionresultlink_ram_indicators.id;


--
-- Name: partners_interventionsectorlocationlink; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_interventionsectorlocationlink (
    id integer NOT NULL,
    intervention_id integer NOT NULL,
    sector_id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL
);


--
-- Name: partners_interventionsectorlocationlink_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_interventionsectorlocationlink_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_interventionsectorlocationlink_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_interventionsectorlocationlink_id_seq OWNED BY chad.partners_interventionsectorlocationlink.id;


--
-- Name: partners_interventionsectorlocationlink_locations; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_interventionsectorlocationlink_locations (
    id integer NOT NULL,
    interventionsectorlocationlink_id integer NOT NULL,
    location_id integer NOT NULL
);


--
-- Name: partners_interventionsectorlocationlink_locations_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_interventionsectorlocationlink_locations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_interventionsectorlocationlink_locations_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_interventionsectorlocationlink_locations_id_seq OWNED BY chad.partners_interventionsectorlocationlink_locations.id;


--
-- Name: partners_partnerorganization; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_partnerorganization (
    id integer NOT NULL,
    partner_type character varying(50) NOT NULL,
    cso_type character varying(50),
    name character varying(255) NOT NULL,
    short_name character varying(50) NOT NULL,
    description character varying(256) NOT NULL,
    address text,
    email character varying(255),
    phone_number character varying(64),
    vendor_number character varying(30),
    alternate_id integer,
    alternate_name character varying(255),
    rating character varying(50),
    type_of_assessment character varying(50),
    last_assessment_date date,
    core_values_assessment_date date,
    core_values_assessment character varying(1024),
    vision_synced boolean NOT NULL,
    hidden boolean NOT NULL,
    deleted_flag boolean NOT NULL,
    total_ct_cp numeric(20,2),
    total_ct_cy numeric(20,2),
    blocked boolean NOT NULL,
    city character varying(64),
    country character varying(64),
    postal_code character varying(32),
    shared_with character varying(20)[],
    street_address character varying(500),
    hact_values jsonb,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    net_ct_cy numeric(20,2),
    reported_cy numeric(20,2),
    total_ct_ytd numeric(20,2),
    basis_for_risk_rating character varying(50) NOT NULL,
    manually_blocked boolean NOT NULL
);


--
-- Name: partners_partnerorganization_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_partnerorganization_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_partnerorganization_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_partnerorganization_id_seq OWNED BY chad.partners_partnerorganization.id;


--
-- Name: partners_partnerplannedvisits; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_partnerplannedvisits (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    year integer NOT NULL,
    programmatic_q1 integer NOT NULL,
    programmatic_q2 integer NOT NULL,
    programmatic_q3 integer NOT NULL,
    programmatic_q4 integer NOT NULL,
    partner_id integer NOT NULL
);


--
-- Name: partners_partnerplannedvisits_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_partnerplannedvisits_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_partnerplannedvisits_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_partnerplannedvisits_id_seq OWNED BY chad.partners_partnerplannedvisits.id;


--
-- Name: partners_partnerstaffmember; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_partnerstaffmember (
    id integer NOT NULL,
    title character varying(64),
    first_name character varying(64) NOT NULL,
    last_name character varying(64) NOT NULL,
    email character varying(128) NOT NULL,
    phone character varying(64),
    active boolean NOT NULL,
    partner_id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL
);


--
-- Name: partners_partnerstaffmember_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_partnerstaffmember_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_partnerstaffmember_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_partnerstaffmember_id_seq OWNED BY chad.partners_partnerstaffmember.id;


--
-- Name: partners_plannedengagement; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_plannedengagement (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    spot_check_planned_q1 integer NOT NULL,
    spot_check_planned_q2 integer NOT NULL,
    spot_check_planned_q3 integer NOT NULL,
    spot_check_planned_q4 integer NOT NULL,
    scheduled_audit boolean NOT NULL,
    special_audit boolean NOT NULL,
    partner_id integer NOT NULL,
    spot_check_follow_up integer NOT NULL
);


--
-- Name: partners_plannedengagement_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_plannedengagement_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_plannedengagement_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_plannedengagement_id_seq OWNED BY chad.partners_plannedengagement.id;


--
-- Name: partners_workspacefiletype; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.partners_workspacefiletype (
    id integer NOT NULL,
    name character varying(64) NOT NULL
);


--
-- Name: partners_workspacefiletype_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.partners_workspacefiletype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: partners_workspacefiletype_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.partners_workspacefiletype_id_seq OWNED BY chad.partners_workspacefiletype.id;


--
-- Name: reports_appliedindicator; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.reports_appliedindicator (
    id integer NOT NULL,
    context_code character varying(50),
    assumptions text,
    total integer,
    indicator_id integer,
    lower_result_id integer NOT NULL,
    means_of_verification character varying(255),
    cluster_indicator_id integer,
    cluster_indicator_title character varying(1024),
    cluster_name character varying(512),
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    response_plan_name character varying(1024),
    section_id integer,
    is_active boolean NOT NULL,
    is_high_frequency boolean NOT NULL,
    baseline jsonb,
    denominator_label character varying(256),
    label text,
    measurement_specifications text,
    numerator_label character varying(256),
    target jsonb NOT NULL,
    CONSTRAINT reports_appliedindicator_cluster_indicator_id_check CHECK ((cluster_indicator_id >= 0))
);


--
-- Name: reports_appliedindicator_disaggregation; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.reports_appliedindicator_disaggregation (
    id integer NOT NULL,
    appliedindicator_id integer NOT NULL,
    disaggregation_id integer NOT NULL
);


--
-- Name: reports_appliedindicator_disaggregation_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.reports_appliedindicator_disaggregation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reports_appliedindicator_disaggregation_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.reports_appliedindicator_disaggregation_id_seq OWNED BY chad.reports_appliedindicator_disaggregation.id;


--
-- Name: reports_appliedindicator_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.reports_appliedindicator_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reports_appliedindicator_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.reports_appliedindicator_id_seq OWNED BY chad.reports_appliedindicator.id;


--
-- Name: reports_appliedindicator_locations; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.reports_appliedindicator_locations (
    id integer NOT NULL,
    appliedindicator_id integer NOT NULL,
    location_id integer NOT NULL
);


--
-- Name: reports_appliedindicator_locations_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.reports_appliedindicator_locations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reports_appliedindicator_locations_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.reports_appliedindicator_locations_id_seq OWNED BY chad.reports_appliedindicator_locations.id;


--
-- Name: reports_countryprogramme; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.reports_countryprogramme (
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    wbs character varying(30) NOT NULL,
    from_date date NOT NULL,
    to_date date NOT NULL,
    invalid boolean NOT NULL
);


--
-- Name: reports_countryprogramme_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.reports_countryprogramme_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reports_countryprogramme_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.reports_countryprogramme_id_seq OWNED BY chad.reports_countryprogramme.id;


--
-- Name: reports_disaggregation; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.reports_disaggregation (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    name character varying(255) NOT NULL,
    active boolean NOT NULL
);


--
-- Name: reports_disaggregation_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.reports_disaggregation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reports_disaggregation_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.reports_disaggregation_id_seq OWNED BY chad.reports_disaggregation.id;


--
-- Name: reports_disaggregationvalue; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.reports_disaggregationvalue (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    value character varying(15) NOT NULL,
    active boolean NOT NULL,
    disaggregation_id integer NOT NULL
);


--
-- Name: reports_disaggregationvalue_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.reports_disaggregationvalue_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reports_disaggregationvalue_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.reports_disaggregationvalue_id_seq OWNED BY chad.reports_disaggregationvalue.id;


--
-- Name: reports_indicator; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.reports_indicator (
    id integer NOT NULL,
    name character varying(1024) NOT NULL,
    code character varying(50),
    total integer,
    sector_total integer,
    current integer,
    sector_current integer,
    assumptions text,
    target character varying(255),
    baseline character varying(255),
    ram_indicator boolean NOT NULL,
    view_on_dashboard boolean NOT NULL,
    result_id integer,
    sector_id integer,
    unit_id integer,
    active boolean NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL
);


--
-- Name: reports_indicator_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.reports_indicator_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reports_indicator_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.reports_indicator_id_seq OWNED BY chad.reports_indicator.id;


--
-- Name: reports_indicatorblueprint; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.reports_indicatorblueprint (
    id integer NOT NULL,
    title character varying(1024) NOT NULL,
    description character varying(3072),
    code character varying(50),
    subdomain character varying(255),
    disaggregatable boolean NOT NULL,
    unit character varying(10) NOT NULL,
    calculation_formula_across_locations character varying(10) NOT NULL,
    calculation_formula_across_periods character varying(10) NOT NULL,
    created timestamp with time zone NOT NULL,
    display_type character varying(10) NOT NULL,
    modified timestamp with time zone NOT NULL
);


--
-- Name: reports_indicatorblueprint_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.reports_indicatorblueprint_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reports_indicatorblueprint_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.reports_indicatorblueprint_id_seq OWNED BY chad.reports_indicatorblueprint.id;


--
-- Name: reports_lowerresult; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.reports_lowerresult (
    id integer NOT NULL,
    name character varying(500) NOT NULL,
    code character varying(50) NOT NULL,
    result_link_id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL
);


--
-- Name: reports_lowerresult_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.reports_lowerresult_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reports_lowerresult_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.reports_lowerresult_id_seq OWNED BY chad.reports_lowerresult.id;


--
-- Name: reports_quarter; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.reports_quarter (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    year character varying(4) NOT NULL,
    start_date timestamp with time zone NOT NULL,
    end_date timestamp with time zone NOT NULL
);


--
-- Name: reports_quarter_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.reports_quarter_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reports_quarter_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.reports_quarter_id_seq OWNED BY chad.reports_quarter.id;


--
-- Name: reports_reportingrequirement; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.reports_reportingrequirement (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    start_date date,
    end_date date,
    due_date date NOT NULL,
    report_type character varying(50) NOT NULL,
    intervention_id integer NOT NULL
);


--
-- Name: reports_reportingrequirement_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.reports_reportingrequirement_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reports_reportingrequirement_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.reports_reportingrequirement_id_seq OWNED BY chad.reports_reportingrequirement.id;


--
-- Name: reports_result; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.reports_result (
    id integer NOT NULL,
    name text NOT NULL,
    code character varying(50),
    from_date date,
    to_date date,
    humanitarian_tag boolean NOT NULL,
    wbs character varying(50),
    vision_id character varying(10),
    gic_code character varying(8),
    gic_name character varying(255),
    sic_code character varying(8),
    sic_name character varying(255),
    activity_focus_code character varying(8),
    activity_focus_name character varying(255),
    hidden boolean NOT NULL,
    ram boolean NOT NULL,
    lft integer NOT NULL,
    rght integer NOT NULL,
    tree_id integer NOT NULL,
    level integer NOT NULL,
    country_programme_id integer,
    parent_id integer,
    result_type_id integer NOT NULL,
    sector_id integer,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    CONSTRAINT reports_result_level_check CHECK ((level >= 0)),
    CONSTRAINT reports_result_lft_check CHECK ((lft >= 0)),
    CONSTRAINT reports_result_rght_check CHECK ((rght >= 0)),
    CONSTRAINT reports_result_tree_id_check CHECK ((tree_id >= 0))
);


--
-- Name: reports_result_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.reports_result_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reports_result_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.reports_result_id_seq OWNED BY chad.reports_result.id;


--
-- Name: reports_resulttype; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.reports_resulttype (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


--
-- Name: reports_resulttype_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.reports_resulttype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reports_resulttype_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.reports_resulttype_id_seq OWNED BY chad.reports_resulttype.id;


--
-- Name: reports_sector; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.reports_sector (
    id integer NOT NULL,
    name character varying(45) NOT NULL,
    description character varying(256),
    alternate_id integer,
    alternate_name character varying(255),
    dashboard boolean NOT NULL,
    color character varying(7),
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL
);


--
-- Name: reports_sector_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.reports_sector_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reports_sector_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.reports_sector_id_seq OWNED BY chad.reports_sector.id;


--
-- Name: reports_specialreportingrequirement; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.reports_specialreportingrequirement (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    description character varying(256) NOT NULL,
    due_date date NOT NULL,
    intervention_id integer NOT NULL
);


--
-- Name: reports_specialreportingrequirement_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.reports_specialreportingrequirement_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reports_specialreportingrequirement_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.reports_specialreportingrequirement_id_seq OWNED BY chad.reports_specialreportingrequirement.id;


--
-- Name: reports_unit; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.reports_unit (
    id integer NOT NULL,
    type character varying(45) NOT NULL
);


--
-- Name: reports_unit_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.reports_unit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reports_unit_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.reports_unit_id_seq OWNED BY chad.reports_unit.id;


--
-- Name: reversion_revision; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.reversion_revision (
    id integer NOT NULL,
    manager_slug character varying(191) NOT NULL,
    date_created timestamp with time zone NOT NULL,
    comment text NOT NULL,
    user_id integer
);


--
-- Name: reversion_revision_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.reversion_revision_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reversion_revision_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.reversion_revision_id_seq OWNED BY chad.reversion_revision.id;


--
-- Name: reversion_version; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.reversion_version (
    id integer NOT NULL,
    object_id text NOT NULL,
    object_id_int integer,
    format character varying(255) NOT NULL,
    serialized_data text NOT NULL,
    object_repr text NOT NULL,
    content_type_id integer NOT NULL,
    revision_id integer NOT NULL
);


--
-- Name: reversion_version_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.reversion_version_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reversion_version_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.reversion_version_id_seq OWNED BY chad.reversion_version.id;


--
-- Name: snapshot_activity; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.snapshot_activity (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    target_object_id character varying(255) NOT NULL,
    action character varying(50) NOT NULL,
    data jsonb NOT NULL,
    change jsonb NOT NULL,
    by_user_id integer NOT NULL,
    target_content_type_id integer NOT NULL
);


--
-- Name: snapshot_activity_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.snapshot_activity_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: snapshot_activity_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.snapshot_activity_id_seq OWNED BY chad.snapshot_activity.id;


--
-- Name: t2f_actionpoint; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.t2f_actionpoint (
    id integer NOT NULL,
    action_point_number character varying(11) NOT NULL,
    description character varying(254) NOT NULL,
    due_date timestamp with time zone NOT NULL,
    status character varying(254) NOT NULL,
    completed_at timestamp with time zone,
    actions_taken text NOT NULL,
    follow_up boolean NOT NULL,
    comments text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    assigned_by_id integer NOT NULL,
    person_responsible_id integer NOT NULL,
    travel_id integer NOT NULL
);


--
-- Name: t2f_actionpoint_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.t2f_actionpoint_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t2f_actionpoint_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.t2f_actionpoint_id_seq OWNED BY chad.t2f_actionpoint.id;


--
-- Name: t2f_clearances; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.t2f_clearances (
    id integer NOT NULL,
    medical_clearance character varying(14) NOT NULL,
    security_clearance character varying(14) NOT NULL,
    security_course character varying(14) NOT NULL,
    travel_id integer NOT NULL
);


--
-- Name: t2f_clearances_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.t2f_clearances_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t2f_clearances_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.t2f_clearances_id_seq OWNED BY chad.t2f_clearances.id;


--
-- Name: t2f_costassignment; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.t2f_costassignment (
    id integer NOT NULL,
    share integer NOT NULL,
    delegate boolean NOT NULL,
    business_area_id integer,
    fund_id integer,
    grant_id integer,
    travel_id integer NOT NULL,
    wbs_id integer,
    CONSTRAINT t2f_costassignment_share_check CHECK ((share >= 0))
);


--
-- Name: t2f_costassignment_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.t2f_costassignment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t2f_costassignment_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.t2f_costassignment_id_seq OWNED BY chad.t2f_costassignment.id;


--
-- Name: t2f_deduction; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.t2f_deduction (
    id integer NOT NULL,
    date date NOT NULL,
    breakfast boolean NOT NULL,
    lunch boolean NOT NULL,
    dinner boolean NOT NULL,
    accomodation boolean NOT NULL,
    no_dsa boolean NOT NULL,
    travel_id integer NOT NULL
);


--
-- Name: t2f_deduction_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.t2f_deduction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t2f_deduction_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.t2f_deduction_id_seq OWNED BY chad.t2f_deduction.id;


--
-- Name: t2f_expense; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.t2f_expense (
    id integer NOT NULL,
    amount numeric(10,4),
    currency_id integer,
    travel_id integer NOT NULL,
    type_id integer
);


--
-- Name: t2f_expense_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.t2f_expense_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t2f_expense_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.t2f_expense_id_seq OWNED BY chad.t2f_expense.id;


--
-- Name: t2f_invoice; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.t2f_invoice (
    id integer NOT NULL,
    reference_number character varying(32) NOT NULL,
    business_area character varying(32) NOT NULL,
    vendor_number character varying(32) NOT NULL,
    amount numeric(20,4) NOT NULL,
    status character varying(16) NOT NULL,
    vision_fi_id character varying(16) NOT NULL,
    currency_id integer NOT NULL,
    travel_id integer NOT NULL,
    messages text[] NOT NULL
);


--
-- Name: t2f_invoice_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.t2f_invoice_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t2f_invoice_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.t2f_invoice_id_seq OWNED BY chad.t2f_invoice.id;


--
-- Name: t2f_invoiceitem; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.t2f_invoiceitem (
    id integer NOT NULL,
    amount numeric(20,10) NOT NULL,
    fund_id integer,
    grant_id integer,
    invoice_id integer NOT NULL,
    wbs_id integer
);


--
-- Name: t2f_invoiceitem_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.t2f_invoiceitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t2f_invoiceitem_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.t2f_invoiceitem_id_seq OWNED BY chad.t2f_invoiceitem.id;


--
-- Name: t2f_itineraryitem_airlines; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.t2f_itineraryitem_airlines (
    id integer NOT NULL,
    itineraryitem_id integer NOT NULL,
    airlinecompany_id integer NOT NULL
);


--
-- Name: t2f_iteneraryitem_airlines_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.t2f_iteneraryitem_airlines_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t2f_iteneraryitem_airlines_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.t2f_iteneraryitem_airlines_id_seq OWNED BY chad.t2f_itineraryitem_airlines.id;


--
-- Name: t2f_itineraryitem; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.t2f_itineraryitem (
    id integer NOT NULL,
    origin character varying(255) NOT NULL,
    destination character varying(255) NOT NULL,
    departure_date timestamp with time zone NOT NULL,
    arrival_date timestamp with time zone NOT NULL,
    overnight_travel boolean NOT NULL,
    mode_of_travel character varying(5) NOT NULL,
    dsa_region_id integer,
    travel_id integer NOT NULL,
    _order integer NOT NULL
);


--
-- Name: t2f_iteneraryitem_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.t2f_iteneraryitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t2f_iteneraryitem_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.t2f_iteneraryitem_id_seq OWNED BY chad.t2f_itineraryitem.id;


--
-- Name: t2f_travel; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.t2f_travel (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    completed_at timestamp with time zone,
    canceled_at timestamp with time zone,
    submitted_at timestamp with time zone,
    rejected_at timestamp with time zone,
    approved_at timestamp with time zone,
    rejection_note text NOT NULL,
    cancellation_note text NOT NULL,
    certification_note text NOT NULL,
    report_note text NOT NULL,
    misc_expenses text NOT NULL,
    status character varying(50) NOT NULL,
    start_date timestamp with time zone,
    end_date timestamp with time zone,
    purpose character varying(500) NOT NULL,
    additional_note text NOT NULL,
    international_travel boolean,
    ta_required boolean,
    reference_number character varying(12) NOT NULL,
    hidden boolean NOT NULL,
    mode_of_travel character varying(5)[],
    estimated_travel_cost numeric(20,4) NOT NULL,
    is_driver boolean NOT NULL,
    preserved_expenses_local numeric(20,4),
    approved_cost_traveler numeric(20,4),
    approved_cost_travel_agencies numeric(20,4),
    currency_id integer,
    office_id integer,
    supervisor_id integer,
    traveler_id integer,
    first_submission_date timestamp with time zone,
    preserved_expenses_usd numeric(20,4),
    section_id integer
);


--
-- Name: t2f_travel_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.t2f_travel_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t2f_travel_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.t2f_travel_id_seq OWNED BY chad.t2f_travel.id;


--
-- Name: t2f_travelactivity; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.t2f_travelactivity (
    id integer NOT NULL,
    travel_type character varying(64) NOT NULL,
    date timestamp with time zone,
    partner_id integer,
    partnership_id integer,
    primary_traveler_id integer NOT NULL,
    result_id integer
);


--
-- Name: t2f_travelactivity_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.t2f_travelactivity_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t2f_travelactivity_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.t2f_travelactivity_id_seq OWNED BY chad.t2f_travelactivity.id;


--
-- Name: t2f_travelactivity_locations; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.t2f_travelactivity_locations (
    id integer NOT NULL,
    travelactivity_id integer NOT NULL,
    location_id integer NOT NULL
);


--
-- Name: t2f_travelactivity_locations_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.t2f_travelactivity_locations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t2f_travelactivity_locations_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.t2f_travelactivity_locations_id_seq OWNED BY chad.t2f_travelactivity_locations.id;


--
-- Name: t2f_travelactivity_travels; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.t2f_travelactivity_travels (
    id integer NOT NULL,
    travelactivity_id integer NOT NULL,
    travel_id integer NOT NULL
);


--
-- Name: t2f_travelactivity_travels_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.t2f_travelactivity_travels_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t2f_travelactivity_travels_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.t2f_travelactivity_travels_id_seq OWNED BY chad.t2f_travelactivity_travels.id;


--
-- Name: t2f_travelattachment; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.t2f_travelattachment (
    id integer NOT NULL,
    type character varying(64) NOT NULL,
    name character varying(255) NOT NULL,
    file character varying(255) NOT NULL,
    travel_id integer NOT NULL
);


--
-- Name: t2f_travelattachment_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.t2f_travelattachment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t2f_travelattachment_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.t2f_travelattachment_id_seq OWNED BY chad.t2f_travelattachment.id;


--
-- Name: tpm_tpmactivity; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.tpm_tpmactivity (
    activity_ptr_id integer NOT NULL,
    additional_information text NOT NULL,
    is_pv boolean NOT NULL,
    tpm_visit_id integer NOT NULL,
    section_id integer NOT NULL
);


--
-- Name: tpm_tpmactivity_offices; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.tpm_tpmactivity_offices (
    id integer NOT NULL,
    tpmactivity_id integer NOT NULL,
    office_id integer NOT NULL
);


--
-- Name: tpm_tpmactivity_offices_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.tpm_tpmactivity_offices_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tpm_tpmactivity_offices_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.tpm_tpmactivity_offices_id_seq OWNED BY chad.tpm_tpmactivity_offices.id;


--
-- Name: tpm_tpmactivity_unicef_focal_points; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.tpm_tpmactivity_unicef_focal_points (
    id integer NOT NULL,
    tpmactivity_id integer NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: tpm_tpmactivity_unicef_focal_points_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.tpm_tpmactivity_unicef_focal_points_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tpm_tpmactivity_unicef_focal_points_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.tpm_tpmactivity_unicef_focal_points_id_seq OWNED BY chad.tpm_tpmactivity_unicef_focal_points.id;


--
-- Name: tpm_tpmvisit; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.tpm_tpmvisit (
    id integer NOT NULL,
    deleted_at timestamp with time zone NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    status character varying(20) NOT NULL,
    reject_comment text NOT NULL,
    approval_comment text NOT NULL,
    visit_information text NOT NULL,
    date_of_assigned date,
    date_of_cancelled date,
    date_of_tpm_accepted date,
    date_of_tpm_rejected date,
    date_of_tpm_reported date,
    date_of_tpm_report_rejected date,
    date_of_unicef_approved date,
    tpm_partner_id integer,
    cancel_comment text NOT NULL,
    author_id integer
);


--
-- Name: tpm_tpmvisit_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.tpm_tpmvisit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tpm_tpmvisit_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.tpm_tpmvisit_id_seq OWNED BY chad.tpm_tpmvisit.id;


--
-- Name: tpm_tpmvisit_tpm_partner_focal_points; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.tpm_tpmvisit_tpm_partner_focal_points (
    id integer NOT NULL,
    tpmvisit_id integer NOT NULL,
    tpmpartnerstaffmember_id integer NOT NULL
);


--
-- Name: tpm_tpmvisit_tpm_partner_focal_points1_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.tpm_tpmvisit_tpm_partner_focal_points1_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tpm_tpmvisit_tpm_partner_focal_points1_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.tpm_tpmvisit_tpm_partner_focal_points1_id_seq OWNED BY chad.tpm_tpmvisit_tpm_partner_focal_points.id;


--
-- Name: tpm_tpmvisitreportrejectcomment; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.tpm_tpmvisitreportrejectcomment (
    id integer NOT NULL,
    rejected_at timestamp with time zone NOT NULL,
    reject_reason text NOT NULL,
    tpm_visit_id integer NOT NULL
);


--
-- Name: tpm_tpmvisitreportrejectcomment_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.tpm_tpmvisitreportrejectcomment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tpm_tpmvisitreportrejectcomment_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.tpm_tpmvisitreportrejectcomment_id_seq OWNED BY chad.tpm_tpmvisitreportrejectcomment.id;


--
-- Name: unicef_snapshot_activity; Type: TABLE; Schema: chad; Owner: -
--

CREATE TABLE chad.unicef_snapshot_activity (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    target_object_id character varying(255) NOT NULL,
    action character varying(50) NOT NULL,
    data jsonb NOT NULL,
    change jsonb NOT NULL,
    by_user_id integer NOT NULL,
    target_content_type_id integer NOT NULL
);


--
-- Name: unicef_snapshot_activity_id_seq; Type: SEQUENCE; Schema: chad; Owner: -
--

CREATE SEQUENCE chad.unicef_snapshot_activity_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: unicef_snapshot_activity_id_seq; Type: SEQUENCE OWNED BY; Schema: chad; Owner: -
--

ALTER SEQUENCE chad.unicef_snapshot_activity_id_seq OWNED BY chad.unicef_snapshot_activity.id;


--
-- Name: action_points_actionpoint id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.action_points_actionpoint ALTER COLUMN id SET DEFAULT nextval('chad.action_points_actionpoint_id_seq'::regclass);


--
-- Name: activities_activity id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.activities_activity ALTER COLUMN id SET DEFAULT nextval('chad.activities_activity_id_seq'::regclass);


--
-- Name: activities_activity_locations id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.activities_activity_locations ALTER COLUMN id SET DEFAULT nextval('chad.activities_activity_locations_id_seq'::regclass);


--
-- Name: actstream_action id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.actstream_action ALTER COLUMN id SET DEFAULT nextval('chad.actstream_action_id_seq'::regclass);


--
-- Name: actstream_follow id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.actstream_follow ALTER COLUMN id SET DEFAULT nextval('chad.actstream_follow_id_seq'::regclass);


--
-- Name: attachments_attachment id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.attachments_attachment ALTER COLUMN id SET DEFAULT nextval('chad.attachments_attachment_id_seq'::regclass);


--
-- Name: attachments_attachmentflat id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.attachments_attachmentflat ALTER COLUMN id SET DEFAULT nextval('chad.attachments_attachmentflat_id_seq'::regclass);


--
-- Name: attachments_filetype id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.attachments_filetype ALTER COLUMN id SET DEFAULT nextval('chad.attachments_filetype_id_seq'::regclass);


--
-- Name: audit_detailedfindinginfo id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_detailedfindinginfo ALTER COLUMN id SET DEFAULT nextval('chad.audit_detailedfindinginfo_id_seq'::regclass);


--
-- Name: audit_engagement id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_engagement ALTER COLUMN id SET DEFAULT nextval('chad.audit_engagement_id_seq'::regclass);


--
-- Name: audit_engagement_active_pd id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_engagement_active_pd ALTER COLUMN id SET DEFAULT nextval('chad.audit_engagement_active_pd_id_seq'::regclass);


--
-- Name: audit_engagement_authorized_officers id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_engagement_authorized_officers ALTER COLUMN id SET DEFAULT nextval('chad.audit_engagement_authorized_officers_id_seq'::regclass);


--
-- Name: audit_engagement_staff_members id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_engagement_staff_members ALTER COLUMN id SET DEFAULT nextval('chad.audit_engagement_staff_members1_id_seq'::regclass);


--
-- Name: audit_financialfinding id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_financialfinding ALTER COLUMN id SET DEFAULT nextval('chad.audit_financialfinding_id_seq'::regclass);


--
-- Name: audit_finding id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_finding ALTER COLUMN id SET DEFAULT nextval('chad.audit_finding_id_seq'::regclass);


--
-- Name: audit_keyinternalcontrol id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_keyinternalcontrol ALTER COLUMN id SET DEFAULT nextval('chad.audit_keyinternalcontrol_id_seq'::regclass);


--
-- Name: audit_risk id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_risk ALTER COLUMN id SET DEFAULT nextval('chad.audit_risk_id_seq'::regclass);


--
-- Name: audit_riskblueprint id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_riskblueprint ALTER COLUMN id SET DEFAULT nextval('chad.audit_riskblueprint_id_seq'::regclass);


--
-- Name: audit_riskcategory id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_riskcategory ALTER COLUMN id SET DEFAULT nextval('chad.audit_riskcategory_id_seq'::regclass);


--
-- Name: audit_specialauditrecommendation id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_specialauditrecommendation ALTER COLUMN id SET DEFAULT nextval('chad.audit_specialauditrecommendation_id_seq'::regclass);


--
-- Name: audit_specificprocedure id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_specificprocedure ALTER COLUMN id SET DEFAULT nextval('chad.audit_specificprocedure_id_seq'::regclass);


--
-- Name: django_comment_flags id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.django_comment_flags ALTER COLUMN id SET DEFAULT nextval('chad.django_comment_flags_id_seq'::regclass);


--
-- Name: django_comments id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.django_comments ALTER COLUMN id SET DEFAULT nextval('chad.django_comments_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.django_migrations ALTER COLUMN id SET DEFAULT nextval('chad.django_migrations_id_seq'::regclass);


--
-- Name: funds_donor id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_donor ALTER COLUMN id SET DEFAULT nextval('chad.funds_donor_id_seq'::regclass);


--
-- Name: funds_fundscommitmentheader id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_fundscommitmentheader ALTER COLUMN id SET DEFAULT nextval('chad.funds_fundscommitmentheader_id_seq'::regclass);


--
-- Name: funds_fundscommitmentitem id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_fundscommitmentitem ALTER COLUMN id SET DEFAULT nextval('chad.funds_fundscommitmentitem_id_seq'::regclass);


--
-- Name: funds_fundsreservationheader id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_fundsreservationheader ALTER COLUMN id SET DEFAULT nextval('chad.funds_fundsreservationheader_id_seq'::regclass);


--
-- Name: funds_fundsreservationitem id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_fundsreservationitem ALTER COLUMN id SET DEFAULT nextval('chad.funds_fundsreservationitem_id_seq'::regclass);


--
-- Name: funds_grant id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_grant ALTER COLUMN id SET DEFAULT nextval('chad.funds_grant_id_seq'::regclass);


--
-- Name: hact_aggregatehact id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.hact_aggregatehact ALTER COLUMN id SET DEFAULT nextval('chad.hact_aggregatehact_id_seq'::regclass);


--
-- Name: hact_hacthistory id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.hact_hacthistory ALTER COLUMN id SET DEFAULT nextval('chad.hact_hacthistory_id_seq'::regclass);


--
-- Name: locations_cartodbtable id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.locations_cartodbtable ALTER COLUMN id SET DEFAULT nextval('chad.locations_cartodbtable_id_seq'::regclass);


--
-- Name: locations_gatewaytype id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.locations_gatewaytype ALTER COLUMN id SET DEFAULT nextval('chad.locations_gatewaytype_id_seq'::regclass);


--
-- Name: locations_location id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.locations_location ALTER COLUMN id SET DEFAULT nextval('chad.locations_location_id_seq'::regclass);


--
-- Name: management_flaggedissue id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.management_flaggedissue ALTER COLUMN id SET DEFAULT nextval('chad.management_flaggedissue_id_seq'::regclass);


--
-- Name: partners_agreement id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_agreement ALTER COLUMN id SET DEFAULT nextval('chad.partners_agreement_id_seq'::regclass);


--
-- Name: partners_agreement_authorized_officers id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_agreement_authorized_officers ALTER COLUMN id SET DEFAULT nextval('chad.partners_agreement_authorized_officers_id_seq'::regclass);


--
-- Name: partners_agreementamendment id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_agreementamendment ALTER COLUMN id SET DEFAULT nextval('chad.partners_agreementamendment_id_seq'::regclass);


--
-- Name: partners_assessment id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_assessment ALTER COLUMN id SET DEFAULT nextval('chad.partners_assessment_id_seq'::regclass);


--
-- Name: partners_corevaluesassessment id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_corevaluesassessment ALTER COLUMN id SET DEFAULT nextval('chad.partners_corevaluesassessment_id_seq'::regclass);


--
-- Name: partners_directcashtransfer id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_directcashtransfer ALTER COLUMN id SET DEFAULT nextval('chad.partners_directcashtransfer_id_seq'::regclass);


--
-- Name: partners_filetype id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_filetype ALTER COLUMN id SET DEFAULT nextval('chad.partners_filetype_id_seq'::regclass);


--
-- Name: partners_fundingcommitment id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_fundingcommitment ALTER COLUMN id SET DEFAULT nextval('chad.partners_fundingcommitment_id_seq'::regclass);


--
-- Name: partners_intervention id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention ALTER COLUMN id SET DEFAULT nextval('chad.partners_intervention_id_seq'::regclass);


--
-- Name: partners_intervention_flat_locations id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_flat_locations ALTER COLUMN id SET DEFAULT nextval('chad.partners_intervention_flat_locations_id_seq'::regclass);


--
-- Name: partners_intervention_offices id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_offices ALTER COLUMN id SET DEFAULT nextval('chad.partners_intervention_offices_id_seq'::regclass);


--
-- Name: partners_intervention_partner_focal_points id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_partner_focal_points ALTER COLUMN id SET DEFAULT nextval('chad.partners_intervention_partner_focal_points_id_seq'::regclass);


--
-- Name: partners_intervention_sections id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_sections ALTER COLUMN id SET DEFAULT nextval('chad.partners_intervention_sections_id_seq'::regclass);


--
-- Name: partners_intervention_unicef_focal_points id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_unicef_focal_points ALTER COLUMN id SET DEFAULT nextval('chad.partners_intervention_unicef_focal_points_id_seq'::regclass);


--
-- Name: partners_interventionamendment id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionamendment ALTER COLUMN id SET DEFAULT nextval('chad.partners_interventionamendment_id_seq'::regclass);


--
-- Name: partners_interventionattachment id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionattachment ALTER COLUMN id SET DEFAULT nextval('chad.partners_interventionattachment_id_seq'::regclass);


--
-- Name: partners_interventionbudget id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionbudget ALTER COLUMN id SET DEFAULT nextval('chad.partners_interventionbudget_id_seq'::regclass);


--
-- Name: partners_interventionplannedvisits id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionplannedvisits ALTER COLUMN id SET DEFAULT nextval('chad.partners_interventionplannedvisits_id_seq'::regclass);


--
-- Name: partners_interventionreportingperiod id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionreportingperiod ALTER COLUMN id SET DEFAULT nextval('chad.partners_interventionreportingperiod_id_seq'::regclass);


--
-- Name: partners_interventionresultlink id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionresultlink ALTER COLUMN id SET DEFAULT nextval('chad.partners_interventionresultlink_id_seq'::regclass);


--
-- Name: partners_interventionresultlink_ram_indicators id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionresultlink_ram_indicators ALTER COLUMN id SET DEFAULT nextval('chad.partners_interventionresultlink_ram_indicators_id_seq'::regclass);


--
-- Name: partners_interventionsectorlocationlink id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionsectorlocationlink ALTER COLUMN id SET DEFAULT nextval('chad.partners_interventionsectorlocationlink_id_seq'::regclass);


--
-- Name: partners_interventionsectorlocationlink_locations id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionsectorlocationlink_locations ALTER COLUMN id SET DEFAULT nextval('chad.partners_interventionsectorlocationlink_locations_id_seq'::regclass);


--
-- Name: partners_partnerorganization id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_partnerorganization ALTER COLUMN id SET DEFAULT nextval('chad.partners_partnerorganization_id_seq'::regclass);


--
-- Name: partners_partnerplannedvisits id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_partnerplannedvisits ALTER COLUMN id SET DEFAULT nextval('chad.partners_partnerplannedvisits_id_seq'::regclass);


--
-- Name: partners_partnerstaffmember id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_partnerstaffmember ALTER COLUMN id SET DEFAULT nextval('chad.partners_partnerstaffmember_id_seq'::regclass);


--
-- Name: partners_plannedengagement id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_plannedengagement ALTER COLUMN id SET DEFAULT nextval('chad.partners_plannedengagement_id_seq'::regclass);


--
-- Name: partners_workspacefiletype id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_workspacefiletype ALTER COLUMN id SET DEFAULT nextval('chad.partners_workspacefiletype_id_seq'::regclass);


--
-- Name: reports_appliedindicator id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_appliedindicator ALTER COLUMN id SET DEFAULT nextval('chad.reports_appliedindicator_id_seq'::regclass);


--
-- Name: reports_appliedindicator_disaggregation id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_appliedindicator_disaggregation ALTER COLUMN id SET DEFAULT nextval('chad.reports_appliedindicator_disaggregation_id_seq'::regclass);


--
-- Name: reports_appliedindicator_locations id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_appliedindicator_locations ALTER COLUMN id SET DEFAULT nextval('chad.reports_appliedindicator_locations_id_seq'::regclass);


--
-- Name: reports_countryprogramme id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_countryprogramme ALTER COLUMN id SET DEFAULT nextval('chad.reports_countryprogramme_id_seq'::regclass);


--
-- Name: reports_disaggregation id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_disaggregation ALTER COLUMN id SET DEFAULT nextval('chad.reports_disaggregation_id_seq'::regclass);


--
-- Name: reports_disaggregationvalue id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_disaggregationvalue ALTER COLUMN id SET DEFAULT nextval('chad.reports_disaggregationvalue_id_seq'::regclass);


--
-- Name: reports_indicator id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_indicator ALTER COLUMN id SET DEFAULT nextval('chad.reports_indicator_id_seq'::regclass);


--
-- Name: reports_indicatorblueprint id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_indicatorblueprint ALTER COLUMN id SET DEFAULT nextval('chad.reports_indicatorblueprint_id_seq'::regclass);


--
-- Name: reports_lowerresult id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_lowerresult ALTER COLUMN id SET DEFAULT nextval('chad.reports_lowerresult_id_seq'::regclass);


--
-- Name: reports_quarter id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_quarter ALTER COLUMN id SET DEFAULT nextval('chad.reports_quarter_id_seq'::regclass);


--
-- Name: reports_reportingrequirement id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_reportingrequirement ALTER COLUMN id SET DEFAULT nextval('chad.reports_reportingrequirement_id_seq'::regclass);


--
-- Name: reports_result id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_result ALTER COLUMN id SET DEFAULT nextval('chad.reports_result_id_seq'::regclass);


--
-- Name: reports_resulttype id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_resulttype ALTER COLUMN id SET DEFAULT nextval('chad.reports_resulttype_id_seq'::regclass);


--
-- Name: reports_sector id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_sector ALTER COLUMN id SET DEFAULT nextval('chad.reports_sector_id_seq'::regclass);


--
-- Name: reports_specialreportingrequirement id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_specialreportingrequirement ALTER COLUMN id SET DEFAULT nextval('chad.reports_specialreportingrequirement_id_seq'::regclass);


--
-- Name: reports_unit id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_unit ALTER COLUMN id SET DEFAULT nextval('chad.reports_unit_id_seq'::regclass);


--
-- Name: reversion_revision id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reversion_revision ALTER COLUMN id SET DEFAULT nextval('chad.reversion_revision_id_seq'::regclass);


--
-- Name: reversion_version id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reversion_version ALTER COLUMN id SET DEFAULT nextval('chad.reversion_version_id_seq'::regclass);


--
-- Name: snapshot_activity id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.snapshot_activity ALTER COLUMN id SET DEFAULT nextval('chad.snapshot_activity_id_seq'::regclass);


--
-- Name: t2f_actionpoint id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_actionpoint ALTER COLUMN id SET DEFAULT nextval('chad.t2f_actionpoint_id_seq'::regclass);


--
-- Name: t2f_clearances id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_clearances ALTER COLUMN id SET DEFAULT nextval('chad.t2f_clearances_id_seq'::regclass);


--
-- Name: t2f_costassignment id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_costassignment ALTER COLUMN id SET DEFAULT nextval('chad.t2f_costassignment_id_seq'::regclass);


--
-- Name: t2f_deduction id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_deduction ALTER COLUMN id SET DEFAULT nextval('chad.t2f_deduction_id_seq'::regclass);


--
-- Name: t2f_expense id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_expense ALTER COLUMN id SET DEFAULT nextval('chad.t2f_expense_id_seq'::regclass);


--
-- Name: t2f_invoice id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_invoice ALTER COLUMN id SET DEFAULT nextval('chad.t2f_invoice_id_seq'::regclass);


--
-- Name: t2f_invoiceitem id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_invoiceitem ALTER COLUMN id SET DEFAULT nextval('chad.t2f_invoiceitem_id_seq'::regclass);


--
-- Name: t2f_itineraryitem id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_itineraryitem ALTER COLUMN id SET DEFAULT nextval('chad.t2f_iteneraryitem_id_seq'::regclass);


--
-- Name: t2f_itineraryitem_airlines id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_itineraryitem_airlines ALTER COLUMN id SET DEFAULT nextval('chad.t2f_iteneraryitem_airlines_id_seq'::regclass);


--
-- Name: t2f_travel id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travel ALTER COLUMN id SET DEFAULT nextval('chad.t2f_travel_id_seq'::regclass);


--
-- Name: t2f_travelactivity id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travelactivity ALTER COLUMN id SET DEFAULT nextval('chad.t2f_travelactivity_id_seq'::regclass);


--
-- Name: t2f_travelactivity_locations id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travelactivity_locations ALTER COLUMN id SET DEFAULT nextval('chad.t2f_travelactivity_locations_id_seq'::regclass);


--
-- Name: t2f_travelactivity_travels id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travelactivity_travels ALTER COLUMN id SET DEFAULT nextval('chad.t2f_travelactivity_travels_id_seq'::regclass);


--
-- Name: t2f_travelattachment id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travelattachment ALTER COLUMN id SET DEFAULT nextval('chad.t2f_travelattachment_id_seq'::regclass);


--
-- Name: tpm_tpmactivity_offices id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmactivity_offices ALTER COLUMN id SET DEFAULT nextval('chad.tpm_tpmactivity_offices_id_seq'::regclass);


--
-- Name: tpm_tpmactivity_unicef_focal_points id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmactivity_unicef_focal_points ALTER COLUMN id SET DEFAULT nextval('chad.tpm_tpmactivity_unicef_focal_points_id_seq'::regclass);


--
-- Name: tpm_tpmvisit id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmvisit ALTER COLUMN id SET DEFAULT nextval('chad.tpm_tpmvisit_id_seq'::regclass);


--
-- Name: tpm_tpmvisit_tpm_partner_focal_points id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmvisit_tpm_partner_focal_points ALTER COLUMN id SET DEFAULT nextval('chad.tpm_tpmvisit_tpm_partner_focal_points1_id_seq'::regclass);


--
-- Name: tpm_tpmvisitreportrejectcomment id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmvisitreportrejectcomment ALTER COLUMN id SET DEFAULT nextval('chad.tpm_tpmvisitreportrejectcomment_id_seq'::regclass);


--
-- Name: unicef_snapshot_activity id; Type: DEFAULT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.unicef_snapshot_activity ALTER COLUMN id SET DEFAULT nextval('chad.unicef_snapshot_activity_id_seq'::regclass);


--
-- Name: action_points_actionpoint action_points_actionpoint_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.action_points_actionpoint
    ADD CONSTRAINT action_points_actionpoint_pkey PRIMARY KEY (id);


--
-- Name: activities_activity_locations activities_activity_locations_activity_id_f8cd5b9e_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.activities_activity_locations
    ADD CONSTRAINT activities_activity_locations_activity_id_f8cd5b9e_uniq UNIQUE (activity_id, location_id);


--
-- Name: activities_activity_locations activities_activity_locations_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.activities_activity_locations
    ADD CONSTRAINT activities_activity_locations_pkey PRIMARY KEY (id);


--
-- Name: activities_activity activities_activity_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.activities_activity
    ADD CONSTRAINT activities_activity_pkey PRIMARY KEY (id);


--
-- Name: actstream_action actstream_action_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.actstream_action
    ADD CONSTRAINT actstream_action_pkey PRIMARY KEY (id);


--
-- Name: actstream_follow actstream_follow_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.actstream_follow
    ADD CONSTRAINT actstream_follow_pkey PRIMARY KEY (id);


--
-- Name: actstream_follow actstream_follow_user_id_63ca7c27_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.actstream_follow
    ADD CONSTRAINT actstream_follow_user_id_63ca7c27_uniq UNIQUE (user_id, content_type_id, object_id);


--
-- Name: attachments_attachment attachments_attachment_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.attachments_attachment
    ADD CONSTRAINT attachments_attachment_pkey PRIMARY KEY (id);


--
-- Name: attachments_attachmentflat attachments_attachmentflat_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.attachments_attachmentflat
    ADD CONSTRAINT attachments_attachmentflat_pkey PRIMARY KEY (id);


--
-- Name: attachments_filetype attachments_filetype_name_83f82570_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.attachments_filetype
    ADD CONSTRAINT attachments_filetype_name_83f82570_uniq UNIQUE (name, code);


--
-- Name: attachments_filetype attachments_filetype_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.attachments_filetype
    ADD CONSTRAINT attachments_filetype_pkey PRIMARY KEY (id);


--
-- Name: audit_audit audit_audit_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_audit
    ADD CONSTRAINT audit_audit_pkey PRIMARY KEY (engagement_ptr_id);


--
-- Name: audit_detailedfindinginfo audit_detailedfindinginfo_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_detailedfindinginfo
    ADD CONSTRAINT audit_detailedfindinginfo_pkey PRIMARY KEY (id);


--
-- Name: audit_engagement_active_pd audit_engagement_active_pd_engagement_id_9fe6cffc_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_engagement_active_pd
    ADD CONSTRAINT audit_engagement_active_pd_engagement_id_9fe6cffc_uniq UNIQUE (engagement_id, intervention_id);


--
-- Name: audit_engagement_active_pd audit_engagement_active_pd_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_engagement_active_pd
    ADD CONSTRAINT audit_engagement_active_pd_pkey PRIMARY KEY (id);


--
-- Name: audit_engagement_authorized_officers audit_engagement_authorized_officer_engagement_id_7dbed7f5_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_engagement_authorized_officers
    ADD CONSTRAINT audit_engagement_authorized_officer_engagement_id_7dbed7f5_uniq UNIQUE (engagement_id, partnerstaffmember_id);


--
-- Name: audit_engagement_authorized_officers audit_engagement_authorized_officers_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_engagement_authorized_officers
    ADD CONSTRAINT audit_engagement_authorized_officers_pkey PRIMARY KEY (id);


--
-- Name: audit_engagement audit_engagement_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_engagement
    ADD CONSTRAINT audit_engagement_pkey PRIMARY KEY (id);


--
-- Name: audit_engagement_staff_members audit_engagement_staff_members1_engagement_id_fa85c846_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_engagement_staff_members
    ADD CONSTRAINT audit_engagement_staff_members1_engagement_id_fa85c846_uniq UNIQUE (engagement_id, auditorstaffmember_id);


--
-- Name: audit_engagement_staff_members audit_engagement_staff_members1_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_engagement_staff_members
    ADD CONSTRAINT audit_engagement_staff_members1_pkey PRIMARY KEY (id);


--
-- Name: audit_financialfinding audit_financialfinding_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_financialfinding
    ADD CONSTRAINT audit_financialfinding_pkey PRIMARY KEY (id);


--
-- Name: audit_finding audit_finding_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_finding
    ADD CONSTRAINT audit_finding_pkey PRIMARY KEY (id);


--
-- Name: audit_keyinternalcontrol audit_keyinternalcontrol_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_keyinternalcontrol
    ADD CONSTRAINT audit_keyinternalcontrol_pkey PRIMARY KEY (id);


--
-- Name: audit_microassessment audit_microassessment_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_microassessment
    ADD CONSTRAINT audit_microassessment_pkey PRIMARY KEY (engagement_ptr_id);


--
-- Name: audit_risk audit_risk_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_risk
    ADD CONSTRAINT audit_risk_pkey PRIMARY KEY (id);


--
-- Name: audit_riskblueprint audit_riskblueprint_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_riskblueprint
    ADD CONSTRAINT audit_riskblueprint_pkey PRIMARY KEY (id);


--
-- Name: audit_riskcategory audit_riskcategory_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_riskcategory
    ADD CONSTRAINT audit_riskcategory_pkey PRIMARY KEY (id);


--
-- Name: audit_specialaudit audit_specialaudit_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_specialaudit
    ADD CONSTRAINT audit_specialaudit_pkey PRIMARY KEY (engagement_ptr_id);


--
-- Name: audit_specialauditrecommendation audit_specialauditrecommendation_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_specialauditrecommendation
    ADD CONSTRAINT audit_specialauditrecommendation_pkey PRIMARY KEY (id);


--
-- Name: audit_specificprocedure audit_specificprocedure_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_specificprocedure
    ADD CONSTRAINT audit_specificprocedure_pkey PRIMARY KEY (id);


--
-- Name: audit_spotcheck audit_spotcheck_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_spotcheck
    ADD CONSTRAINT audit_spotcheck_pkey PRIMARY KEY (engagement_ptr_id);


--
-- Name: django_comment_flags django_comment_flags_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.django_comment_flags
    ADD CONSTRAINT django_comment_flags_pkey PRIMARY KEY (id);


--
-- Name: django_comment_flags django_comment_flags_user_id_537f77a7_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.django_comment_flags
    ADD CONSTRAINT django_comment_flags_user_id_537f77a7_uniq UNIQUE (user_id, comment_id, flag);


--
-- Name: django_comments django_comments_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.django_comments
    ADD CONSTRAINT django_comments_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: funds_donor funds_donor_name_key; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_donor
    ADD CONSTRAINT funds_donor_name_key UNIQUE (name);


--
-- Name: funds_donor funds_donor_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_donor
    ADD CONSTRAINT funds_donor_pkey PRIMARY KEY (id);


--
-- Name: funds_fundscommitmentheader funds_fundscommitmentheader_fc_number_f5605368_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_fundscommitmentheader
    ADD CONSTRAINT funds_fundscommitmentheader_fc_number_f5605368_uniq UNIQUE (fc_number);


--
-- Name: funds_fundscommitmentheader funds_fundscommitmentheader_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_fundscommitmentheader
    ADD CONSTRAINT funds_fundscommitmentheader_pkey PRIMARY KEY (id);


--
-- Name: funds_fundscommitmentitem funds_fundscommitmentitem_fund_commitment_id_013ea496_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_fundscommitmentitem
    ADD CONSTRAINT funds_fundscommitmentitem_fund_commitment_id_013ea496_uniq UNIQUE (fund_commitment_id, line_item);


--
-- Name: funds_fundscommitmentitem funds_fundscommitmentitem_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_fundscommitmentitem
    ADD CONSTRAINT funds_fundscommitmentitem_pkey PRIMARY KEY (id);


--
-- Name: funds_fundsreservationheader funds_fundsreservationheader_fr_number_key; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_fundsreservationheader
    ADD CONSTRAINT funds_fundsreservationheader_fr_number_key UNIQUE (fr_number);


--
-- Name: funds_fundsreservationheader funds_fundsreservationheader_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_fundsreservationheader
    ADD CONSTRAINT funds_fundsreservationheader_pkey PRIMARY KEY (id);


--
-- Name: funds_fundsreservationheader funds_fundsreservationheader_vendor_code_50244998_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_fundsreservationheader
    ADD CONSTRAINT funds_fundsreservationheader_vendor_code_50244998_uniq UNIQUE (vendor_code, fr_number);


--
-- Name: funds_fundsreservationitem funds_fundsreservationitem_fund_reservation_id_1abda768_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_fundsreservationitem
    ADD CONSTRAINT funds_fundsreservationitem_fund_reservation_id_1abda768_uniq UNIQUE (fund_reservation_id, line_item);


--
-- Name: funds_fundsreservationitem funds_fundsreservationitem_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_fundsreservationitem
    ADD CONSTRAINT funds_fundsreservationitem_pkey PRIMARY KEY (id);


--
-- Name: funds_grant funds_grant_name_key; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_grant
    ADD CONSTRAINT funds_grant_name_key UNIQUE (name);


--
-- Name: funds_grant funds_grant_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_grant
    ADD CONSTRAINT funds_grant_pkey PRIMARY KEY (id);


--
-- Name: hact_aggregatehact hact_aggregatehact_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.hact_aggregatehact
    ADD CONSTRAINT hact_aggregatehact_pkey PRIMARY KEY (id);


--
-- Name: hact_aggregatehact hact_aggregatehact_year_key; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.hact_aggregatehact
    ADD CONSTRAINT hact_aggregatehact_year_key UNIQUE (year);


--
-- Name: hact_hacthistory hact_hacthistory_partner_id_4fe148dc_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.hact_hacthistory
    ADD CONSTRAINT hact_hacthistory_partner_id_4fe148dc_uniq UNIQUE (partner_id, year);


--
-- Name: hact_hacthistory hact_hacthistory_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.hact_hacthistory
    ADD CONSTRAINT hact_hacthistory_pkey PRIMARY KEY (id);


--
-- Name: locations_cartodbtable locations_cartodbtable_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.locations_cartodbtable
    ADD CONSTRAINT locations_cartodbtable_pkey PRIMARY KEY (id);


--
-- Name: locations_gatewaytype locations_gatewaytype_admin_level_key; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.locations_gatewaytype
    ADD CONSTRAINT locations_gatewaytype_admin_level_key UNIQUE (admin_level);


--
-- Name: locations_gatewaytype locations_gatewaytype_name_key; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.locations_gatewaytype
    ADD CONSTRAINT locations_gatewaytype_name_key UNIQUE (name);


--
-- Name: locations_gatewaytype locations_gatewaytype_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.locations_gatewaytype
    ADD CONSTRAINT locations_gatewaytype_pkey PRIMARY KEY (id);


--
-- Name: locations_location locations_location_name_fc4d5026_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.locations_location
    ADD CONSTRAINT locations_location_name_fc4d5026_uniq UNIQUE (name, gateway_id, p_code);


--
-- Name: locations_location locations_location_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.locations_location
    ADD CONSTRAINT locations_location_pkey PRIMARY KEY (id);


--
-- Name: management_flaggedissue management_flaggedissue_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.management_flaggedissue
    ADD CONSTRAINT management_flaggedissue_pkey PRIMARY KEY (id);


--
-- Name: partners_agreement partners_agreement_agreement_number_05f1f99e_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_agreement
    ADD CONSTRAINT partners_agreement_agreement_number_05f1f99e_uniq UNIQUE (agreement_number);


--
-- Name: partners_agreement_authorized_officers partners_agreement_authorized_office_agreement_id_f93f7ee1_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_agreement_authorized_officers
    ADD CONSTRAINT partners_agreement_authorized_office_agreement_id_f93f7ee1_uniq UNIQUE (agreement_id, partnerstaffmember_id);


--
-- Name: partners_agreement_authorized_officers partners_agreement_authorized_officers_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_agreement_authorized_officers
    ADD CONSTRAINT partners_agreement_authorized_officers_pkey PRIMARY KEY (id);


--
-- Name: partners_agreement partners_agreement_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_agreement
    ADD CONSTRAINT partners_agreement_pkey PRIMARY KEY (id);


--
-- Name: partners_agreementamendment partners_agreementamendment_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_agreementamendment
    ADD CONSTRAINT partners_agreementamendment_pkey PRIMARY KEY (id);


--
-- Name: partners_assessment partners_assessment_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_assessment
    ADD CONSTRAINT partners_assessment_pkey PRIMARY KEY (id);


--
-- Name: partners_corevaluesassessment partners_corevaluesassessment_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_corevaluesassessment
    ADD CONSTRAINT partners_corevaluesassessment_pkey PRIMARY KEY (id);


--
-- Name: partners_directcashtransfer partners_directcashtransfer_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_directcashtransfer
    ADD CONSTRAINT partners_directcashtransfer_pkey PRIMARY KEY (id);


--
-- Name: partners_filetype partners_filetype_name_key; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_filetype
    ADD CONSTRAINT partners_filetype_name_key UNIQUE (name);


--
-- Name: partners_filetype partners_filetype_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_filetype
    ADD CONSTRAINT partners_filetype_pkey PRIMARY KEY (id);


--
-- Name: partners_fundingcommitment partners_fundingcommitment_fc_ref_key; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_fundingcommitment
    ADD CONSTRAINT partners_fundingcommitment_fc_ref_key UNIQUE (fc_ref);


--
-- Name: partners_fundingcommitment partners_fundingcommitment_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_fundingcommitment
    ADD CONSTRAINT partners_fundingcommitment_pkey PRIMARY KEY (id);


--
-- Name: partners_interventionsectorlocationlink_locations partners_interv_interventionsectorlocationlink_id_40f4e298_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionsectorlocationlink_locations
    ADD CONSTRAINT partners_interv_interventionsectorlocationlink_id_40f4e298_uniq UNIQUE (interventionsectorlocationlink_id, location_id);


--
-- Name: partners_intervention_flat_locations partners_intervention_flat_locati_intervention_id_b0bfcf1a_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_flat_locations
    ADD CONSTRAINT partners_intervention_flat_locati_intervention_id_b0bfcf1a_uniq UNIQUE (intervention_id, location_id);


--
-- Name: partners_intervention_flat_locations partners_intervention_flat_locations_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_flat_locations
    ADD CONSTRAINT partners_intervention_flat_locations_pkey PRIMARY KEY (id);


--
-- Name: partners_intervention partners_intervention_number_780b39ca_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention
    ADD CONSTRAINT partners_intervention_number_780b39ca_uniq UNIQUE (number);


--
-- Name: partners_intervention_offices partners_intervention_offices_intervention_id_f0e3f18c_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_offices
    ADD CONSTRAINT partners_intervention_offices_intervention_id_f0e3f18c_uniq UNIQUE (intervention_id, office_id);


--
-- Name: partners_intervention_offices partners_intervention_offices_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_offices
    ADD CONSTRAINT partners_intervention_offices_pkey PRIMARY KEY (id);


--
-- Name: partners_intervention_partner_focal_points partners_intervention_partner_foc_intervention_id_eccad0fd_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_partner_focal_points
    ADD CONSTRAINT partners_intervention_partner_foc_intervention_id_eccad0fd_uniq UNIQUE (intervention_id, partnerstaffmember_id);


--
-- Name: partners_intervention_partner_focal_points partners_intervention_partner_focal_points_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_partner_focal_points
    ADD CONSTRAINT partners_intervention_partner_focal_points_pkey PRIMARY KEY (id);


--
-- Name: partners_intervention partners_intervention_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention
    ADD CONSTRAINT partners_intervention_pkey PRIMARY KEY (id);


--
-- Name: partners_intervention_sections partners_intervention_sections_intervention_id_d0e206bf_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_sections
    ADD CONSTRAINT partners_intervention_sections_intervention_id_d0e206bf_uniq UNIQUE (intervention_id, sector_id);


--
-- Name: partners_intervention_sections partners_intervention_sections_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_sections
    ADD CONSTRAINT partners_intervention_sections_pkey PRIMARY KEY (id);


--
-- Name: partners_intervention_unicef_focal_points partners_intervention_unicef_foca_intervention_id_75084ddb_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_unicef_focal_points
    ADD CONSTRAINT partners_intervention_unicef_foca_intervention_id_75084ddb_uniq UNIQUE (intervention_id, user_id);


--
-- Name: partners_intervention_unicef_focal_points partners_intervention_unicef_focal_points_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_unicef_focal_points
    ADD CONSTRAINT partners_intervention_unicef_focal_points_pkey PRIMARY KEY (id);


--
-- Name: partners_interventionamendment partners_interventionamendment_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionamendment
    ADD CONSTRAINT partners_interventionamendment_pkey PRIMARY KEY (id);


--
-- Name: partners_interventionattachment partners_interventionattachment_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionattachment
    ADD CONSTRAINT partners_interventionattachment_pkey PRIMARY KEY (id);


--
-- Name: partners_interventionbudget partners_interventionbudget_intervention_id_4b2f53ff_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionbudget
    ADD CONSTRAINT partners_interventionbudget_intervention_id_4b2f53ff_uniq UNIQUE (intervention_id);


--
-- Name: partners_interventionbudget partners_interventionbudget_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionbudget
    ADD CONSTRAINT partners_interventionbudget_pkey PRIMARY KEY (id);


--
-- Name: partners_interventionplannedvisits partners_interventionplannedvisit_intervention_id_98c06ad5_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionplannedvisits
    ADD CONSTRAINT partners_interventionplannedvisit_intervention_id_98c06ad5_uniq UNIQUE (intervention_id, year);


--
-- Name: partners_interventionplannedvisits partners_interventionplannedvisits_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionplannedvisits
    ADD CONSTRAINT partners_interventionplannedvisits_pkey PRIMARY KEY (id);


--
-- Name: partners_interventionresultlink_ram_indicators partners_interventionre_interventionresultlink_id_7e12c2bb_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionresultlink_ram_indicators
    ADD CONSTRAINT partners_interventionre_interventionresultlink_id_7e12c2bb_uniq UNIQUE (interventionresultlink_id, indicator_id);


--
-- Name: partners_interventionreportingperiod partners_interventionreportingperiod_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionreportingperiod
    ADD CONSTRAINT partners_interventionreportingperiod_pkey PRIMARY KEY (id);


--
-- Name: partners_interventionresultlink partners_interventionresultlink_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionresultlink
    ADD CONSTRAINT partners_interventionresultlink_pkey PRIMARY KEY (id);


--
-- Name: partners_interventionresultlink_ram_indicators partners_interventionresultlink_ram_indicators_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionresultlink_ram_indicators
    ADD CONSTRAINT partners_interventionresultlink_ram_indicators_pkey PRIMARY KEY (id);


--
-- Name: partners_interventionsectorlocationlink_locations partners_interventionsectorlocationlink_locations_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionsectorlocationlink_locations
    ADD CONSTRAINT partners_interventionsectorlocationlink_locations_pkey PRIMARY KEY (id);


--
-- Name: partners_interventionsectorlocationlink partners_interventionsectorlocationlink_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionsectorlocationlink
    ADD CONSTRAINT partners_interventionsectorlocationlink_pkey PRIMARY KEY (id);


--
-- Name: partners_partnerorganization partners_partnerorganization_name_70cf01b1_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_partnerorganization
    ADD CONSTRAINT partners_partnerorganization_name_70cf01b1_uniq UNIQUE (name, vendor_number);


--
-- Name: partners_partnerorganization partners_partnerorganization_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_partnerorganization
    ADD CONSTRAINT partners_partnerorganization_pkey PRIMARY KEY (id);


--
-- Name: partners_partnerorganization partners_partnerorganization_vendor_number_key; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_partnerorganization
    ADD CONSTRAINT partners_partnerorganization_vendor_number_key UNIQUE (vendor_number);


--
-- Name: partners_partnerplannedvisits partners_partnerplannedvisits_partner_id_eeb06e4d_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_partnerplannedvisits
    ADD CONSTRAINT partners_partnerplannedvisits_partner_id_eeb06e4d_uniq UNIQUE (partner_id, year);


--
-- Name: partners_partnerplannedvisits partners_partnerplannedvisits_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_partnerplannedvisits
    ADD CONSTRAINT partners_partnerplannedvisits_pkey PRIMARY KEY (id);


--
-- Name: partners_partnerstaffmember partners_partnerstaffmember_email_key; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_partnerstaffmember
    ADD CONSTRAINT partners_partnerstaffmember_email_key UNIQUE (email);


--
-- Name: partners_partnerstaffmember partners_partnerstaffmember_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_partnerstaffmember
    ADD CONSTRAINT partners_partnerstaffmember_pkey PRIMARY KEY (id);


--
-- Name: partners_plannedengagement partners_plannedengagement_partner_id_key; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_plannedengagement
    ADD CONSTRAINT partners_plannedengagement_partner_id_key UNIQUE (partner_id);


--
-- Name: partners_plannedengagement partners_plannedengagement_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_plannedengagement
    ADD CONSTRAINT partners_plannedengagement_pkey PRIMARY KEY (id);


--
-- Name: partners_workspacefiletype partners_workspacefiletype_name_key; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_workspacefiletype
    ADD CONSTRAINT partners_workspacefiletype_name_key UNIQUE (name);


--
-- Name: partners_workspacefiletype partners_workspacefiletype_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_workspacefiletype
    ADD CONSTRAINT partners_workspacefiletype_pkey PRIMARY KEY (id);


--
-- Name: reports_appliedindicator_disaggregation reports_appliedindicator_disa_appliedindicator_id_81ad568c_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_appliedindicator_disaggregation
    ADD CONSTRAINT reports_appliedindicator_disa_appliedindicator_id_81ad568c_uniq UNIQUE (appliedindicator_id, disaggregation_id);


--
-- Name: reports_appliedindicator_disaggregation reports_appliedindicator_disaggregation_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_appliedindicator_disaggregation
    ADD CONSTRAINT reports_appliedindicator_disaggregation_pkey PRIMARY KEY (id);


--
-- Name: reports_appliedindicator reports_appliedindicator_indicator_id_8556cd81_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_appliedindicator
    ADD CONSTRAINT reports_appliedindicator_indicator_id_8556cd81_uniq UNIQUE (indicator_id, lower_result_id);


--
-- Name: reports_appliedindicator_locations reports_appliedindicator_loca_appliedindicator_id_224962ba_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_appliedindicator_locations
    ADD CONSTRAINT reports_appliedindicator_loca_appliedindicator_id_224962ba_uniq UNIQUE (appliedindicator_id, location_id);


--
-- Name: reports_appliedindicator_locations reports_appliedindicator_locations_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_appliedindicator_locations
    ADD CONSTRAINT reports_appliedindicator_locations_pkey PRIMARY KEY (id);


--
-- Name: reports_appliedindicator reports_appliedindicator_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_appliedindicator
    ADD CONSTRAINT reports_appliedindicator_pkey PRIMARY KEY (id);


--
-- Name: reports_countryprogramme reports_countryprogramme_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_countryprogramme
    ADD CONSTRAINT reports_countryprogramme_pkey PRIMARY KEY (id);


--
-- Name: reports_countryprogramme reports_countryprogramme_wbs_key; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_countryprogramme
    ADD CONSTRAINT reports_countryprogramme_wbs_key UNIQUE (wbs);


--
-- Name: reports_disaggregation reports_disaggregation_name_key; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_disaggregation
    ADD CONSTRAINT reports_disaggregation_name_key UNIQUE (name);


--
-- Name: reports_disaggregation reports_disaggregation_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_disaggregation
    ADD CONSTRAINT reports_disaggregation_pkey PRIMARY KEY (id);


--
-- Name: reports_disaggregationvalue reports_disaggregationvalue_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_disaggregationvalue
    ADD CONSTRAINT reports_disaggregationvalue_pkey PRIMARY KEY (id);


--
-- Name: reports_indicator reports_indicator_name_3791d838_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_indicator
    ADD CONSTRAINT reports_indicator_name_3791d838_uniq UNIQUE (name, result_id, sector_id);


--
-- Name: reports_indicator reports_indicator_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_indicator
    ADD CONSTRAINT reports_indicator_pkey PRIMARY KEY (id);


--
-- Name: reports_indicatorblueprint reports_indicatorblueprint_code_key; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_indicatorblueprint
    ADD CONSTRAINT reports_indicatorblueprint_code_key UNIQUE (code);


--
-- Name: reports_indicatorblueprint reports_indicatorblueprint_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_indicatorblueprint
    ADD CONSTRAINT reports_indicatorblueprint_pkey PRIMARY KEY (id);


--
-- Name: reports_lowerresult reports_lowerresult_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_lowerresult
    ADD CONSTRAINT reports_lowerresult_pkey PRIMARY KEY (id);


--
-- Name: reports_lowerresult reports_lowerresult_result_link_id_1e72f118_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_lowerresult
    ADD CONSTRAINT reports_lowerresult_result_link_id_1e72f118_uniq UNIQUE (result_link_id, code);


--
-- Name: reports_quarter reports_quarter_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_quarter
    ADD CONSTRAINT reports_quarter_pkey PRIMARY KEY (id);


--
-- Name: reports_reportingrequirement reports_reportingrequirement_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_reportingrequirement
    ADD CONSTRAINT reports_reportingrequirement_pkey PRIMARY KEY (id);


--
-- Name: reports_result reports_result_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_result
    ADD CONSTRAINT reports_result_pkey PRIMARY KEY (id);


--
-- Name: reports_result reports_result_wbs_ce8feefd_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_result
    ADD CONSTRAINT reports_result_wbs_ce8feefd_uniq UNIQUE (wbs, country_programme_id);


--
-- Name: reports_resulttype reports_resulttype_name_key; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_resulttype
    ADD CONSTRAINT reports_resulttype_name_key UNIQUE (name);


--
-- Name: reports_resulttype reports_resulttype_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_resulttype
    ADD CONSTRAINT reports_resulttype_pkey PRIMARY KEY (id);


--
-- Name: reports_sector reports_sector_name_key; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_sector
    ADD CONSTRAINT reports_sector_name_key UNIQUE (name);


--
-- Name: reports_sector reports_sector_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_sector
    ADD CONSTRAINT reports_sector_pkey PRIMARY KEY (id);


--
-- Name: reports_specialreportingrequirement reports_specialreportingrequirement_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_specialreportingrequirement
    ADD CONSTRAINT reports_specialreportingrequirement_pkey PRIMARY KEY (id);


--
-- Name: reports_unit reports_unit_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_unit
    ADD CONSTRAINT reports_unit_pkey PRIMARY KEY (id);


--
-- Name: reports_unit reports_unit_type_key; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_unit
    ADD CONSTRAINT reports_unit_type_key UNIQUE (type);


--
-- Name: reversion_revision reversion_revision_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reversion_revision
    ADD CONSTRAINT reversion_revision_pkey PRIMARY KEY (id);


--
-- Name: reversion_version reversion_version_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reversion_version
    ADD CONSTRAINT reversion_version_pkey PRIMARY KEY (id);


--
-- Name: snapshot_activity snapshot_activity_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.snapshot_activity
    ADD CONSTRAINT snapshot_activity_pkey PRIMARY KEY (id);


--
-- Name: t2f_actionpoint t2f_actionpoint_action_point_number_key; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_actionpoint
    ADD CONSTRAINT t2f_actionpoint_action_point_number_key UNIQUE (action_point_number);


--
-- Name: t2f_actionpoint t2f_actionpoint_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_actionpoint
    ADD CONSTRAINT t2f_actionpoint_pkey PRIMARY KEY (id);


--
-- Name: t2f_clearances t2f_clearances_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_clearances
    ADD CONSTRAINT t2f_clearances_pkey PRIMARY KEY (id);


--
-- Name: t2f_clearances t2f_clearances_travel_id_key; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_clearances
    ADD CONSTRAINT t2f_clearances_travel_id_key UNIQUE (travel_id);


--
-- Name: t2f_costassignment t2f_costassignment_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_costassignment
    ADD CONSTRAINT t2f_costassignment_pkey PRIMARY KEY (id);


--
-- Name: t2f_deduction t2f_deduction_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_deduction
    ADD CONSTRAINT t2f_deduction_pkey PRIMARY KEY (id);


--
-- Name: t2f_expense t2f_expense_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_expense
    ADD CONSTRAINT t2f_expense_pkey PRIMARY KEY (id);


--
-- Name: t2f_invoice t2f_invoice_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_invoice
    ADD CONSTRAINT t2f_invoice_pkey PRIMARY KEY (id);


--
-- Name: t2f_invoice t2f_invoice_reference_number_key; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_invoice
    ADD CONSTRAINT t2f_invoice_reference_number_key UNIQUE (reference_number);


--
-- Name: t2f_invoiceitem t2f_invoiceitem_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_invoiceitem
    ADD CONSTRAINT t2f_invoiceitem_pkey PRIMARY KEY (id);


--
-- Name: t2f_itineraryitem_airlines t2f_iteneraryitem_airlines_iteneraryitem_id_3f5ee941_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_itineraryitem_airlines
    ADD CONSTRAINT t2f_iteneraryitem_airlines_iteneraryitem_id_3f5ee941_uniq UNIQUE (itineraryitem_id, airlinecompany_id);


--
-- Name: t2f_itineraryitem_airlines t2f_iteneraryitem_airlines_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_itineraryitem_airlines
    ADD CONSTRAINT t2f_iteneraryitem_airlines_pkey PRIMARY KEY (id);


--
-- Name: t2f_itineraryitem t2f_iteneraryitem_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_itineraryitem
    ADD CONSTRAINT t2f_iteneraryitem_pkey PRIMARY KEY (id);


--
-- Name: t2f_travel t2f_travel_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travel
    ADD CONSTRAINT t2f_travel_pkey PRIMARY KEY (id);


--
-- Name: t2f_travel t2f_travel_reference_number_key; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travel
    ADD CONSTRAINT t2f_travel_reference_number_key UNIQUE (reference_number);


--
-- Name: t2f_travelactivity_locations t2f_travelactivity_locations_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travelactivity_locations
    ADD CONSTRAINT t2f_travelactivity_locations_pkey PRIMARY KEY (id);


--
-- Name: t2f_travelactivity_locations t2f_travelactivity_locations_travelactivity_id_e38ac8be_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travelactivity_locations
    ADD CONSTRAINT t2f_travelactivity_locations_travelactivity_id_e38ac8be_uniq UNIQUE (travelactivity_id, location_id);


--
-- Name: t2f_travelactivity t2f_travelactivity_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travelactivity
    ADD CONSTRAINT t2f_travelactivity_pkey PRIMARY KEY (id);


--
-- Name: t2f_travelactivity_travels t2f_travelactivity_travels_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travelactivity_travels
    ADD CONSTRAINT t2f_travelactivity_travels_pkey PRIMARY KEY (id);


--
-- Name: t2f_travelactivity_travels t2f_travelactivity_travels_travelactivity_id_303b6c7a_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travelactivity_travels
    ADD CONSTRAINT t2f_travelactivity_travels_travelactivity_id_303b6c7a_uniq UNIQUE (travelactivity_id, travel_id);


--
-- Name: t2f_travelattachment t2f_travelattachment_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travelattachment
    ADD CONSTRAINT t2f_travelattachment_pkey PRIMARY KEY (id);


--
-- Name: tpm_tpmactivity_offices tpm_tpmactivity_offices_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmactivity_offices
    ADD CONSTRAINT tpm_tpmactivity_offices_pkey PRIMARY KEY (id);


--
-- Name: tpm_tpmactivity_offices tpm_tpmactivity_offices_tpmactivity_id_4e0ba531_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmactivity_offices
    ADD CONSTRAINT tpm_tpmactivity_offices_tpmactivity_id_4e0ba531_uniq UNIQUE (tpmactivity_id, office_id);


--
-- Name: tpm_tpmactivity tpm_tpmactivity_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmactivity
    ADD CONSTRAINT tpm_tpmactivity_pkey PRIMARY KEY (activity_ptr_id);


--
-- Name: tpm_tpmactivity_unicef_focal_points tpm_tpmactivity_unicef_focal_point_tpmactivity_id_7d224d1c_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmactivity_unicef_focal_points
    ADD CONSTRAINT tpm_tpmactivity_unicef_focal_point_tpmactivity_id_7d224d1c_uniq UNIQUE (tpmactivity_id, user_id);


--
-- Name: tpm_tpmactivity_unicef_focal_points tpm_tpmactivity_unicef_focal_points_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmactivity_unicef_focal_points
    ADD CONSTRAINT tpm_tpmactivity_unicef_focal_points_pkey PRIMARY KEY (id);


--
-- Name: tpm_tpmvisit tpm_tpmvisit_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmvisit
    ADD CONSTRAINT tpm_tpmvisit_pkey PRIMARY KEY (id);


--
-- Name: tpm_tpmvisit_tpm_partner_focal_points tpm_tpmvisit_tpm_partner_focal_points1_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmvisit_tpm_partner_focal_points
    ADD CONSTRAINT tpm_tpmvisit_tpm_partner_focal_points1_pkey PRIMARY KEY (id);


--
-- Name: tpm_tpmvisit_tpm_partner_focal_points tpm_tpmvisit_tpm_partner_focal_points_tpmvisit_id_e336a640_uniq; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmvisit_tpm_partner_focal_points
    ADD CONSTRAINT tpm_tpmvisit_tpm_partner_focal_points_tpmvisit_id_e336a640_uniq UNIQUE (tpmvisit_id, tpmpartnerstaffmember_id);


--
-- Name: tpm_tpmvisitreportrejectcomment tpm_tpmvisitreportrejectcomment_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmvisitreportrejectcomment
    ADD CONSTRAINT tpm_tpmvisitreportrejectcomment_pkey PRIMARY KEY (id);


--
-- Name: unicef_snapshot_activity unicef_snapshot_activity_pkey; Type: CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.unicef_snapshot_activity
    ADD CONSTRAINT unicef_snapshot_activity_pkey PRIMARY KEY (id);


--
-- Name: action_points_actionpoint_02c1725c; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX action_points_actionpoint_02c1725c ON chad.action_points_actionpoint USING btree (assigned_to_id);


--
-- Name: action_points_actionpoint_123a1ce7; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX action_points_actionpoint_123a1ce7 ON chad.action_points_actionpoint USING btree (intervention_id);


--
-- Name: action_points_actionpoint_24ec8d02; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX action_points_actionpoint_24ec8d02 ON chad.action_points_actionpoint USING btree (cp_output_id);


--
-- Name: action_points_actionpoint_4e98b6eb; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX action_points_actionpoint_4e98b6eb ON chad.action_points_actionpoint USING btree (partner_id);


--
-- Name: action_points_actionpoint_4f331e2f; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX action_points_actionpoint_4f331e2f ON chad.action_points_actionpoint USING btree (author_id);


--
-- Name: action_points_actionpoint_5f532748; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX action_points_actionpoint_5f532748 ON chad.action_points_actionpoint USING btree (travel_activity_id);


--
-- Name: action_points_actionpoint_730f6511; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX action_points_actionpoint_730f6511 ON chad.action_points_actionpoint USING btree (section_id);


--
-- Name: action_points_actionpoint_a38a7228; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX action_points_actionpoint_a38a7228 ON chad.action_points_actionpoint USING btree (assigned_by_id);


--
-- Name: action_points_actionpoint_cb794678; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX action_points_actionpoint_cb794678 ON chad.action_points_actionpoint USING btree (category_id);


--
-- Name: action_points_actionpoint_cc247b05; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX action_points_actionpoint_cc247b05 ON chad.action_points_actionpoint USING btree (office_id);


--
-- Name: action_points_actionpoint_cd7ada3b; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX action_points_actionpoint_cd7ada3b ON chad.action_points_actionpoint USING btree (engagement_id);


--
-- Name: action_points_actionpoint_e274a5da; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX action_points_actionpoint_e274a5da ON chad.action_points_actionpoint USING btree (location_id);


--
-- Name: action_points_actionpoint_ea71e3b4; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX action_points_actionpoint_ea71e3b4 ON chad.action_points_actionpoint USING btree (tpm_activity_id);


--
-- Name: activities_activity_123a1ce7; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX activities_activity_123a1ce7 ON chad.activities_activity USING btree (intervention_id);


--
-- Name: activities_activity_24ec8d02; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX activities_activity_24ec8d02 ON chad.activities_activity USING btree (cp_output_id);


--
-- Name: activities_activity_4e98b6eb; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX activities_activity_4e98b6eb ON chad.activities_activity USING btree (partner_id);


--
-- Name: activities_activity_locations_e274a5da; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX activities_activity_locations_e274a5da ON chad.activities_activity_locations USING btree (location_id);


--
-- Name: activities_activity_locations_f8a3193a; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX activities_activity_locations_f8a3193a ON chad.activities_activity_locations USING btree (activity_id);


--
-- Name: actstream_action_142874d9; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX actstream_action_142874d9 ON chad.actstream_action USING btree (action_object_content_type_id);


--
-- Name: actstream_action_1cd2a6ae; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX actstream_action_1cd2a6ae ON chad.actstream_action USING btree (target_object_id);


--
-- Name: actstream_action_4c9184f3; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX actstream_action_4c9184f3 ON chad.actstream_action USING btree (public);


--
-- Name: actstream_action_53a09d9a; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX actstream_action_53a09d9a ON chad.actstream_action USING btree (actor_content_type_id);


--
-- Name: actstream_action_9063443c; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX actstream_action_9063443c ON chad.actstream_action USING btree (action_object_object_id);


--
-- Name: actstream_action_action_object_object_id_6433bdf7_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX actstream_action_action_object_object_id_6433bdf7_like ON chad.actstream_action USING btree (action_object_object_id varchar_pattern_ops);


--
-- Name: actstream_action_actor_object_id_72ef0cfa_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX actstream_action_actor_object_id_72ef0cfa_like ON chad.actstream_action USING btree (actor_object_id varchar_pattern_ops);


--
-- Name: actstream_action_b512ddf1; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX actstream_action_b512ddf1 ON chad.actstream_action USING btree (verb);


--
-- Name: actstream_action_c4f7c191; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX actstream_action_c4f7c191 ON chad.actstream_action USING btree (actor_object_id);


--
-- Name: actstream_action_d7e6d55b; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX actstream_action_d7e6d55b ON chad.actstream_action USING btree ("timestamp");


--
-- Name: actstream_action_e4f9dcc7; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX actstream_action_e4f9dcc7 ON chad.actstream_action USING btree (target_content_type_id);


--
-- Name: actstream_action_target_object_id_e080d801_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX actstream_action_target_object_id_e080d801_like ON chad.actstream_action USING btree (target_object_id varchar_pattern_ops);


--
-- Name: actstream_action_verb_83f768b7_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX actstream_action_verb_83f768b7_like ON chad.actstream_action USING btree (verb varchar_pattern_ops);


--
-- Name: actstream_follow_3bebb2f8; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX actstream_follow_3bebb2f8 ON chad.actstream_follow USING btree (started);


--
-- Name: actstream_follow_417f1b1c; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX actstream_follow_417f1b1c ON chad.actstream_follow USING btree (content_type_id);


--
-- Name: actstream_follow_af31437c; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX actstream_follow_af31437c ON chad.actstream_follow USING btree (object_id);


--
-- Name: actstream_follow_e8701ad4; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX actstream_follow_e8701ad4 ON chad.actstream_follow USING btree (user_id);


--
-- Name: actstream_follow_object_id_d790e00d_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX actstream_follow_object_id_d790e00d_like ON chad.actstream_follow USING btree (object_id varchar_pattern_ops);


--
-- Name: attachments_attachment_4095e96b; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX attachments_attachment_4095e96b ON chad.attachments_attachment USING btree (uploaded_by_id);


--
-- Name: attachments_attachment_417f1b1c; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX attachments_attachment_417f1b1c ON chad.attachments_attachment USING btree (content_type_id);


--
-- Name: attachments_attachment_4cc23034; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX attachments_attachment_4cc23034 ON chad.attachments_attachment USING btree (file_type_id);


--
-- Name: attachments_attachmentflat_07ba63f5; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX attachments_attachmentflat_07ba63f5 ON chad.attachments_attachmentflat USING btree (attachment_id);


--
-- Name: attachments_filetype_70a17ffa; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX attachments_filetype_70a17ffa ON chad.attachments_filetype USING btree ("order");


--
-- Name: audit_detailedfindinginfo_9c4e166c; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX audit_detailedfindinginfo_9c4e166c ON chad.audit_detailedfindinginfo USING btree (micro_assesment_id);


--
-- Name: audit_engagement_135bd84a; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX audit_engagement_135bd84a ON chad.audit_engagement USING btree (po_item_id);


--
-- Name: audit_engagement_4e98b6eb; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX audit_engagement_4e98b6eb ON chad.audit_engagement USING btree (partner_id);


--
-- Name: audit_engagement_active_pd_123a1ce7; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX audit_engagement_active_pd_123a1ce7 ON chad.audit_engagement_active_pd USING btree (intervention_id);


--
-- Name: audit_engagement_active_pd_cd7ada3b; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX audit_engagement_active_pd_cd7ada3b ON chad.audit_engagement_active_pd USING btree (engagement_id);


--
-- Name: audit_engagement_authorized_officers_017e2566; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX audit_engagement_authorized_officers_017e2566 ON chad.audit_engagement_authorized_officers USING btree (partnerstaffmember_id);


--
-- Name: audit_engagement_authorized_officers_cd7ada3b; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX audit_engagement_authorized_officers_cd7ada3b ON chad.audit_engagement_authorized_officers USING btree (engagement_id);


--
-- Name: audit_engagement_d80896d1; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX audit_engagement_d80896d1 ON chad.audit_engagement USING btree (agreement_id);


--
-- Name: audit_engagement_staff_members1_7d43d41c; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX audit_engagement_staff_members1_7d43d41c ON chad.audit_engagement_staff_members USING btree (auditorstaffmember_id);


--
-- Name: audit_engagement_staff_members1_cd7ada3b; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX audit_engagement_staff_members1_cd7ada3b ON chad.audit_engagement_staff_members USING btree (engagement_id);


--
-- Name: audit_financialfinding_8b75ec30; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX audit_financialfinding_8b75ec30 ON chad.audit_financialfinding USING btree (audit_id);


--
-- Name: audit_finding_b9577549; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX audit_finding_b9577549 ON chad.audit_finding USING btree (spot_check_id);


--
-- Name: audit_keyinternalcontrol_8b75ec30; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX audit_keyinternalcontrol_8b75ec30 ON chad.audit_keyinternalcontrol USING btree (audit_id);


--
-- Name: audit_risk_2c682e13; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX audit_risk_2c682e13 ON chad.audit_risk USING btree (blueprint_id);


--
-- Name: audit_risk_cd7ada3b; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX audit_risk_cd7ada3b ON chad.audit_risk USING btree (engagement_id);


--
-- Name: audit_riskblueprint_70a17ffa; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX audit_riskblueprint_70a17ffa ON chad.audit_riskblueprint USING btree ("order");


--
-- Name: audit_riskblueprint_b583a629; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX audit_riskblueprint_b583a629 ON chad.audit_riskblueprint USING btree (category_id);


--
-- Name: audit_riskcategory_6be37982; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX audit_riskcategory_6be37982 ON chad.audit_riskcategory USING btree (parent_id);


--
-- Name: audit_riskcategory_70a17ffa; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX audit_riskcategory_70a17ffa ON chad.audit_riskcategory USING btree ("order");


--
-- Name: audit_specialauditrecommendation_8b75ec30; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX audit_specialauditrecommendation_8b75ec30 ON chad.audit_specialauditrecommendation USING btree (audit_id);


--
-- Name: audit_specificprocedure_8b75ec30; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX audit_specificprocedure_8b75ec30 ON chad.audit_specificprocedure USING btree (audit_id);


--
-- Name: django_comment_flags_327a6c43; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX django_comment_flags_327a6c43 ON chad.django_comment_flags USING btree (flag);


--
-- Name: django_comment_flags_69b97d17; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX django_comment_flags_69b97d17 ON chad.django_comment_flags USING btree (comment_id);


--
-- Name: django_comment_flags_e8701ad4; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX django_comment_flags_e8701ad4 ON chad.django_comment_flags USING btree (user_id);


--
-- Name: django_comment_flags_flag_8b141fcb_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX django_comment_flags_flag_8b141fcb_like ON chad.django_comment_flags USING btree (flag varchar_pattern_ops);


--
-- Name: django_comments_417f1b1c; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX django_comments_417f1b1c ON chad.django_comments USING btree (content_type_id);


--
-- Name: django_comments_9365d6e7; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX django_comments_9365d6e7 ON chad.django_comments USING btree (site_id);


--
-- Name: django_comments_e8701ad4; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX django_comments_e8701ad4 ON chad.django_comments USING btree (user_id);


--
-- Name: django_comments_submit_date_514ed2d9_uniq; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX django_comments_submit_date_514ed2d9_uniq ON chad.django_comments USING btree (submit_date);


--
-- Name: funds_donor_name_762a3244_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX funds_donor_name_762a3244_like ON chad.funds_donor USING btree (name varchar_pattern_ops);


--
-- Name: funds_fundscommitmentheader_fc_number_f5605368_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX funds_fundscommitmentheader_fc_number_f5605368_like ON chad.funds_fundscommitmentheader USING btree (fc_number varchar_pattern_ops);


--
-- Name: funds_fundscommitmentitem_eef07b1e; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX funds_fundscommitmentitem_eef07b1e ON chad.funds_fundscommitmentitem USING btree (fund_commitment_id);


--
-- Name: funds_fundsreservationheader_123a1ce7; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX funds_fundsreservationheader_123a1ce7 ON chad.funds_fundsreservationheader USING btree (intervention_id);


--
-- Name: funds_fundsreservationheader_fr_number_d9937013_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX funds_fundsreservationheader_fr_number_d9937013_like ON chad.funds_fundsreservationheader USING btree (fr_number varchar_pattern_ops);


--
-- Name: funds_fundsreservationitem_fd84179f; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX funds_fundsreservationitem_fd84179f ON chad.funds_fundsreservationitem USING btree (fund_reservation_id);


--
-- Name: funds_grant_029df19e; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX funds_grant_029df19e ON chad.funds_grant USING btree (donor_id);


--
-- Name: funds_grant_name_800f6fb1_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX funds_grant_name_800f6fb1_like ON chad.funds_grant USING btree (name varchar_pattern_ops);


--
-- Name: hact_hacthistory_4e98b6eb; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX hact_hacthistory_4e98b6eb ON chad.hact_hacthistory USING btree (partner_id);


--
-- Name: index_locations_on_name_trigram; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX index_locations_on_name_trigram ON chad.locations_location USING gin (name gin_trgm_ops);


--
-- Name: locations_cartodbtable_3cfbd988; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX locations_cartodbtable_3cfbd988 ON chad.locations_cartodbtable USING btree (rght);


--
-- Name: locations_cartodbtable_61737a71; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX locations_cartodbtable_61737a71 ON chad.locations_cartodbtable USING btree (location_type_id);


--
-- Name: locations_cartodbtable_656442a0; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX locations_cartodbtable_656442a0 ON chad.locations_cartodbtable USING btree (tree_id);


--
-- Name: locations_cartodbtable_6be37982; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX locations_cartodbtable_6be37982 ON chad.locations_cartodbtable USING btree (parent_id);


--
-- Name: locations_cartodbtable_c9e9a848; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX locations_cartodbtable_c9e9a848 ON chad.locations_cartodbtable USING btree (level);


--
-- Name: locations_cartodbtable_caf7cc51; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX locations_cartodbtable_caf7cc51 ON chad.locations_cartodbtable USING btree (lft);


--
-- Name: locations_gatewaytype_name_2c9c8fe6_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX locations_gatewaytype_name_2c9c8fe6_like ON chad.locations_gatewaytype USING btree (name varchar_pattern_ops);


--
-- Name: locations_location_1e9cd8d4; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX locations_location_1e9cd8d4 ON chad.locations_location USING btree (gateway_id);


--
-- Name: locations_location_3cfbd988; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX locations_location_3cfbd988 ON chad.locations_location USING btree (rght);


--
-- Name: locations_location_656442a0; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX locations_location_656442a0 ON chad.locations_location USING btree (tree_id);


--
-- Name: locations_location_6be37982; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX locations_location_6be37982 ON chad.locations_location USING btree (parent_id);


--
-- Name: locations_location_c9e9a848; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX locations_location_c9e9a848 ON chad.locations_location USING btree (level);


--
-- Name: locations_location_caf7cc51; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX locations_location_caf7cc51 ON chad.locations_location USING btree (lft);


--
-- Name: locations_location_geom_id; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX locations_location_geom_id ON chad.locations_location USING gist (geom);


--
-- Name: locations_location_point_id; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX locations_location_point_id ON chad.locations_location USING gist (point);


--
-- Name: management_flaggedissue_417f1b1c; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX management_flaggedissue_417f1b1c ON chad.management_flaggedissue USING btree (content_type_id);


--
-- Name: management_flaggedissue_issue_category_1ff4a186_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX management_flaggedissue_issue_category_1ff4a186_like ON chad.management_flaggedissue USING btree (issue_category varchar_pattern_ops);


--
-- Name: management_flaggedissue_issue_category_1ff4a186_uniq; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX management_flaggedissue_issue_category_1ff4a186_uniq ON chad.management_flaggedissue USING btree (issue_category);


--
-- Name: management_flaggedissue_issue_id_a76ff318_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX management_flaggedissue_issue_id_a76ff318_like ON chad.management_flaggedissue USING btree (issue_id varchar_pattern_ops);


--
-- Name: management_flaggedissue_issue_id_a76ff318_uniq; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX management_flaggedissue_issue_id_a76ff318_uniq ON chad.management_flaggedissue USING btree (issue_id);


--
-- Name: management_flaggedissue_issue_status_a53b260a_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX management_flaggedissue_issue_status_a53b260a_like ON chad.management_flaggedissue USING btree (issue_status varchar_pattern_ops);


--
-- Name: management_flaggedissue_issue_status_a53b260a_uniq; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX management_flaggedissue_issue_status_a53b260a_uniq ON chad.management_flaggedissue USING btree (issue_status);


--
-- Name: management_flaggedissue_object_id_2366eab6_uniq; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX management_flaggedissue_object_id_2366eab6_uniq ON chad.management_flaggedissue USING btree (object_id);


--
-- Name: partners_agreement_031ba7c4; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_agreement_031ba7c4 ON chad.partners_agreement USING btree (country_programme_id);


--
-- Name: partners_agreement_4e98b6eb; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_agreement_4e98b6eb ON chad.partners_agreement USING btree (partner_id);


--
-- Name: partners_agreement_7dad813f; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_agreement_7dad813f ON chad.partners_agreement USING btree (partner_manager_id);


--
-- Name: partners_agreement_9f081af4; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_agreement_9f081af4 ON chad.partners_agreement USING btree (signed_by_id);


--
-- Name: partners_agreement_agreement_number_05f1f99e_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_agreement_agreement_number_05f1f99e_like ON chad.partners_agreement USING btree (agreement_number varchar_pattern_ops);


--
-- Name: partners_agreement_authorized_officers_017e2566; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_agreement_authorized_officers_017e2566 ON chad.partners_agreement_authorized_officers USING btree (partnerstaffmember_id);


--
-- Name: partners_agreement_authorized_officers_410cd312; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_agreement_authorized_officers_410cd312 ON chad.partners_agreement_authorized_officers USING btree (agreement_id);


--
-- Name: partners_agreementamendment_410cd312; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_agreementamendment_410cd312 ON chad.partners_agreementamendment USING btree (agreement_id);


--
-- Name: partners_assessment_4e98b6eb; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_assessment_4e98b6eb ON chad.partners_assessment USING btree (partner_id);


--
-- Name: partners_assessment_cd7afc21; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_assessment_cd7afc21 ON chad.partners_assessment USING btree (approving_officer_id);


--
-- Name: partners_assessment_d268de14; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_assessment_d268de14 ON chad.partners_assessment USING btree (requesting_officer_id);


--
-- Name: partners_corevaluesassessment_4e98b6eb; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_corevaluesassessment_4e98b6eb ON chad.partners_corevaluesassessment USING btree (partner_id);


--
-- Name: partners_filetype_name_c4d67350_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_filetype_name_c4d67350_like ON chad.partners_filetype USING btree (name varchar_pattern_ops);


--
-- Name: partners_fundingcommitment_c2418e07; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_fundingcommitment_c2418e07 ON chad.partners_fundingcommitment USING btree (grant_id);


--
-- Name: partners_fundingcommitment_fc_ref_4c1970b6_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_fundingcommitment_fc_ref_4c1970b6_like ON chad.partners_fundingcommitment USING btree (fc_ref varchar_pattern_ops);


--
-- Name: partners_intervention_031ba7c4; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_intervention_031ba7c4 ON chad.partners_intervention USING btree (country_programme_id);


--
-- Name: partners_intervention_410cd312; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_intervention_410cd312 ON chad.partners_intervention USING btree (agreement_id);


--
-- Name: partners_intervention_73c984ba; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_intervention_73c984ba ON chad.partners_intervention USING btree (partner_authorized_officer_signatory_id);


--
-- Name: partners_intervention_ed43f3d6; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_intervention_ed43f3d6 ON chad.partners_intervention USING btree (unicef_signatory_id);


--
-- Name: partners_intervention_flat_locations_123a1ce7; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_intervention_flat_locations_123a1ce7 ON chad.partners_intervention_flat_locations USING btree (intervention_id);


--
-- Name: partners_intervention_flat_locations_e274a5da; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_intervention_flat_locations_e274a5da ON chad.partners_intervention_flat_locations USING btree (location_id);


--
-- Name: partners_intervention_number_780b39ca_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_intervention_number_780b39ca_like ON chad.partners_intervention USING btree (number varchar_pattern_ops);


--
-- Name: partners_intervention_offices_123a1ce7; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_intervention_offices_123a1ce7 ON chad.partners_intervention_offices USING btree (intervention_id);


--
-- Name: partners_intervention_offices_cc247b05; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_intervention_offices_cc247b05 ON chad.partners_intervention_offices USING btree (office_id);


--
-- Name: partners_intervention_partner_focal_points_017e2566; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_intervention_partner_focal_points_017e2566 ON chad.partners_intervention_partner_focal_points USING btree (partnerstaffmember_id);


--
-- Name: partners_intervention_partner_focal_points_123a1ce7; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_intervention_partner_focal_points_123a1ce7 ON chad.partners_intervention_partner_focal_points USING btree (intervention_id);


--
-- Name: partners_intervention_sections_123a1ce7; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_intervention_sections_123a1ce7 ON chad.partners_intervention_sections USING btree (intervention_id);


--
-- Name: partners_intervention_sections_5b1d2adf; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_intervention_sections_5b1d2adf ON chad.partners_intervention_sections USING btree (sector_id);


--
-- Name: partners_intervention_unicef_focal_points_123a1ce7; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_intervention_unicef_focal_points_123a1ce7 ON chad.partners_intervention_unicef_focal_points USING btree (intervention_id);


--
-- Name: partners_intervention_unicef_focal_points_e8701ad4; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_intervention_unicef_focal_points_e8701ad4 ON chad.partners_intervention_unicef_focal_points USING btree (user_id);


--
-- Name: partners_interventionamendment_123a1ce7; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_interventionamendment_123a1ce7 ON chad.partners_interventionamendment USING btree (intervention_id);


--
-- Name: partners_interventionattachment_123a1ce7; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_interventionattachment_123a1ce7 ON chad.partners_interventionattachment USING btree (intervention_id);


--
-- Name: partners_interventionattachment_94757cae; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_interventionattachment_94757cae ON chad.partners_interventionattachment USING btree (type_id);


--
-- Name: partners_interventionbudget_123a1ce7; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_interventionbudget_123a1ce7 ON chad.partners_interventionbudget USING btree (intervention_id);


--
-- Name: partners_interventionplannedvisits_123a1ce7; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_interventionplannedvisits_123a1ce7 ON chad.partners_interventionplannedvisits USING btree (intervention_id);


--
-- Name: partners_interventionreportingperiod_123a1ce7; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_interventionreportingperiod_123a1ce7 ON chad.partners_interventionreportingperiod USING btree (intervention_id);


--
-- Name: partners_interventionresultlink_123a1ce7; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_interventionresultlink_123a1ce7 ON chad.partners_interventionresultlink USING btree (intervention_id);


--
-- Name: partners_interventionresultlink_24ec8d02; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_interventionresultlink_24ec8d02 ON chad.partners_interventionresultlink USING btree (cp_output_id);


--
-- Name: partners_interventionresultlink_ram_indicators_70bff951; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_interventionresultlink_ram_indicators_70bff951 ON chad.partners_interventionresultlink_ram_indicators USING btree (interventionresultlink_id);


--
-- Name: partners_interventionresultlink_ram_indicators_a82bd466; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_interventionresultlink_ram_indicators_a82bd466 ON chad.partners_interventionresultlink_ram_indicators USING btree (indicator_id);


--
-- Name: partners_interventionsectorlocationlink_123a1ce7; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_interventionsectorlocationlink_123a1ce7 ON chad.partners_interventionsectorlocationlink USING btree (intervention_id);


--
-- Name: partners_interventionsectorlocationlink_5b1d2adf; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_interventionsectorlocationlink_5b1d2adf ON chad.partners_interventionsectorlocationlink USING btree (sector_id);


--
-- Name: partners_interventionsectorlocationlink_locations_510c1d46; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_interventionsectorlocationlink_locations_510c1d46 ON chad.partners_interventionsectorlocationlink_locations USING btree (interventionsectorlocationlink_id);


--
-- Name: partners_interventionsectorlocationlink_locations_e274a5da; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_interventionsectorlocationlink_locations_e274a5da ON chad.partners_interventionsectorlocationlink_locations USING btree (location_id);


--
-- Name: partners_partnerorganization_vendor_number_8dce2f98_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_partnerorganization_vendor_number_8dce2f98_like ON chad.partners_partnerorganization USING btree (vendor_number varchar_pattern_ops);


--
-- Name: partners_partnerplannedvisits_4e98b6eb; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_partnerplannedvisits_4e98b6eb ON chad.partners_partnerplannedvisits USING btree (partner_id);


--
-- Name: partners_partnerstaffmember_4e98b6eb; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_partnerstaffmember_4e98b6eb ON chad.partners_partnerstaffmember USING btree (partner_id);


--
-- Name: partners_partnerstaffmember_email_8d2411ec_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_partnerstaffmember_email_8d2411ec_like ON chad.partners_partnerstaffmember USING btree (email varchar_pattern_ops);


--
-- Name: partners_workspacefiletype_name_0247fb9d_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX partners_workspacefiletype_name_0247fb9d_like ON chad.partners_workspacefiletype USING btree (name varchar_pattern_ops);


--
-- Name: reports_appliedindicator_730f6511; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_appliedindicator_730f6511 ON chad.reports_appliedindicator USING btree (section_id);


--
-- Name: reports_appliedindicator_8723fc8a; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_appliedindicator_8723fc8a ON chad.reports_appliedindicator USING btree (lower_result_id);


--
-- Name: reports_appliedindicator_a82bd466; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_appliedindicator_a82bd466 ON chad.reports_appliedindicator USING btree (indicator_id);


--
-- Name: reports_appliedindicator_disaggregation_1f2e43cd; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_appliedindicator_disaggregation_1f2e43cd ON chad.reports_appliedindicator_disaggregation USING btree (appliedindicator_id);


--
-- Name: reports_appliedindicator_disaggregation_972fbe52; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_appliedindicator_disaggregation_972fbe52 ON chad.reports_appliedindicator_disaggregation USING btree (disaggregation_id);


--
-- Name: reports_appliedindicator_locations_1f2e43cd; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_appliedindicator_locations_1f2e43cd ON chad.reports_appliedindicator_locations USING btree (appliedindicator_id);


--
-- Name: reports_appliedindicator_locations_e274a5da; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_appliedindicator_locations_e274a5da ON chad.reports_appliedindicator_locations USING btree (location_id);


--
-- Name: reports_countryprogramme_wbs_c254e3fe_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_countryprogramme_wbs_c254e3fe_like ON chad.reports_countryprogramme USING btree (wbs varchar_pattern_ops);


--
-- Name: reports_disaggregation_name_bfc1feb5_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_disaggregation_name_bfc1feb5_like ON chad.reports_disaggregation USING btree (name varchar_pattern_ops);


--
-- Name: reports_disaggregationvalue_972fbe52; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_disaggregationvalue_972fbe52 ON chad.reports_disaggregationvalue USING btree (disaggregation_id);


--
-- Name: reports_indicator_57f06544; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_indicator_57f06544 ON chad.reports_indicator USING btree (result_id);


--
-- Name: reports_indicator_5b1d2adf; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_indicator_5b1d2adf ON chad.reports_indicator USING btree (sector_id);


--
-- Name: reports_indicator_e8175980; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_indicator_e8175980 ON chad.reports_indicator USING btree (unit_id);


--
-- Name: reports_indicatorblueprint_code_29fadc42_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_indicatorblueprint_code_29fadc42_like ON chad.reports_indicatorblueprint USING btree (code varchar_pattern_ops);


--
-- Name: reports_lowerresult_bde4fd4e; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_lowerresult_bde4fd4e ON chad.reports_lowerresult USING btree (result_link_id);


--
-- Name: reports_reportingrequirement_123a1ce7; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_reportingrequirement_123a1ce7 ON chad.reports_reportingrequirement USING btree (intervention_id);


--
-- Name: reports_result_031ba7c4; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_result_031ba7c4 ON chad.reports_result USING btree (country_programme_id);


--
-- Name: reports_result_3cfbd988; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_result_3cfbd988 ON chad.reports_result USING btree (rght);


--
-- Name: reports_result_5b1d2adf; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_result_5b1d2adf ON chad.reports_result USING btree (sector_id);


--
-- Name: reports_result_656442a0; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_result_656442a0 ON chad.reports_result USING btree (tree_id);


--
-- Name: reports_result_6be37982; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_result_6be37982 ON chad.reports_result USING btree (parent_id);


--
-- Name: reports_result_c9e9a848; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_result_c9e9a848 ON chad.reports_result USING btree (level);


--
-- Name: reports_result_caf7cc51; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_result_caf7cc51 ON chad.reports_result USING btree (lft);


--
-- Name: reports_result_fc36e3fa; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_result_fc36e3fa ON chad.reports_result USING btree (result_type_id);


--
-- Name: reports_resulttype_name_c9902d85_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_resulttype_name_c9902d85_like ON chad.reports_resulttype USING btree (name varchar_pattern_ops);


--
-- Name: reports_sector_name_444a5e3c_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_sector_name_444a5e3c_like ON chad.reports_sector USING btree (name varchar_pattern_ops);


--
-- Name: reports_specialreportingrequirement_123a1ce7; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_specialreportingrequirement_123a1ce7 ON chad.reports_specialreportingrequirement USING btree (intervention_id);


--
-- Name: reports_unit_type_52bb6a6d_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reports_unit_type_52bb6a6d_like ON chad.reports_unit USING btree (type varchar_pattern_ops);


--
-- Name: reversion_revision_b16b0f06; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reversion_revision_b16b0f06 ON chad.reversion_revision USING btree (manager_slug);


--
-- Name: reversion_revision_c69e55a4; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reversion_revision_c69e55a4 ON chad.reversion_revision USING btree (date_created);


--
-- Name: reversion_revision_e8701ad4; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reversion_revision_e8701ad4 ON chad.reversion_revision USING btree (user_id);


--
-- Name: reversion_revision_manager_slug_388da6fe_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reversion_revision_manager_slug_388da6fe_like ON chad.reversion_revision USING btree (manager_slug varchar_pattern_ops);


--
-- Name: reversion_version_0c9ba3a3; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reversion_version_0c9ba3a3 ON chad.reversion_version USING btree (object_id_int);


--
-- Name: reversion_version_417f1b1c; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reversion_version_417f1b1c ON chad.reversion_version USING btree (content_type_id);


--
-- Name: reversion_version_5de09a8d; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX reversion_version_5de09a8d ON chad.reversion_version USING btree (revision_id);


--
-- Name: snapshot_activity_1cd2a6ae; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX snapshot_activity_1cd2a6ae ON chad.snapshot_activity USING btree (target_object_id);


--
-- Name: snapshot_activity_1ef87b2e; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX snapshot_activity_1ef87b2e ON chad.snapshot_activity USING btree (by_user_id);


--
-- Name: snapshot_activity_e4f9dcc7; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX snapshot_activity_e4f9dcc7 ON chad.snapshot_activity USING btree (target_content_type_id);


--
-- Name: snapshot_activity_target_object_id_3a9faef0_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX snapshot_activity_target_object_id_3a9faef0_like ON chad.snapshot_activity USING btree (target_object_id varchar_pattern_ops);


--
-- Name: t2f_actionpoint_18844eba; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_actionpoint_18844eba ON chad.t2f_actionpoint USING btree (person_responsible_id);


--
-- Name: t2f_actionpoint_46413c35; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_actionpoint_46413c35 ON chad.t2f_actionpoint USING btree (travel_id);


--
-- Name: t2f_actionpoint_a38a7228; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_actionpoint_a38a7228 ON chad.t2f_actionpoint USING btree (assigned_by_id);


--
-- Name: t2f_actionpoint_action_point_number_1222d557_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_actionpoint_action_point_number_1222d557_like ON chad.t2f_actionpoint USING btree (action_point_number varchar_pattern_ops);


--
-- Name: t2f_costassignment_46413c35; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_costassignment_46413c35 ON chad.t2f_costassignment USING btree (travel_id);


--
-- Name: t2f_costassignment_4e6789a8; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_costassignment_4e6789a8 ON chad.t2f_costassignment USING btree (fund_id);


--
-- Name: t2f_costassignment_78655e45; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_costassignment_78655e45 ON chad.t2f_costassignment USING btree (wbs_id);


--
-- Name: t2f_costassignment_93469a5b; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_costassignment_93469a5b ON chad.t2f_costassignment USING btree (business_area_id);


--
-- Name: t2f_costassignment_c2418e07; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_costassignment_c2418e07 ON chad.t2f_costassignment USING btree (grant_id);


--
-- Name: t2f_deduction_46413c35; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_deduction_46413c35 ON chad.t2f_deduction USING btree (travel_id);


--
-- Name: t2f_expense_1f21a871; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_expense_1f21a871 ON chad.t2f_expense USING btree (currency_id);


--
-- Name: t2f_expense_46413c35; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_expense_46413c35 ON chad.t2f_expense USING btree (travel_id);


--
-- Name: t2f_expense_94757cae; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_expense_94757cae ON chad.t2f_expense USING btree (type_id);


--
-- Name: t2f_invoice_2c7d5721; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_invoice_2c7d5721 ON chad.t2f_invoice USING btree (currency_id);


--
-- Name: t2f_invoice_46413c35; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_invoice_46413c35 ON chad.t2f_invoice USING btree (travel_id);


--
-- Name: t2f_invoice_reference_number_5197b5f5_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_invoice_reference_number_5197b5f5_like ON chad.t2f_invoice USING btree (reference_number varchar_pattern_ops);


--
-- Name: t2f_invoiceitem_4e6789a8; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_invoiceitem_4e6789a8 ON chad.t2f_invoiceitem USING btree (fund_id);


--
-- Name: t2f_invoiceitem_78655e45; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_invoiceitem_78655e45 ON chad.t2f_invoiceitem USING btree (wbs_id);


--
-- Name: t2f_invoiceitem_c2418e07; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_invoiceitem_c2418e07 ON chad.t2f_invoiceitem USING btree (grant_id);


--
-- Name: t2f_invoiceitem_f1f5d967; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_invoiceitem_f1f5d967 ON chad.t2f_invoiceitem USING btree (invoice_id);


--
-- Name: t2f_iteneraryitem_46413c35; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_iteneraryitem_46413c35 ON chad.t2f_itineraryitem USING btree (travel_id);


--
-- Name: t2f_iteneraryitem_a365bfb2; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_iteneraryitem_a365bfb2 ON chad.t2f_itineraryitem USING btree (dsa_region_id);


--
-- Name: t2f_iteneraryitem_airlines_b8cd2e2b; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_iteneraryitem_airlines_b8cd2e2b ON chad.t2f_itineraryitem_airlines USING btree (itineraryitem_id);


--
-- Name: t2f_iteneraryitem_airlines_fec5ad70; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_iteneraryitem_airlines_fec5ad70 ON chad.t2f_itineraryitem_airlines USING btree (airlinecompany_id);


--
-- Name: t2f_travel_2c7d5721; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_travel_2c7d5721 ON chad.t2f_travel USING btree (currency_id);


--
-- Name: t2f_travel_2e3bcc0e; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_travel_2e3bcc0e ON chad.t2f_travel USING btree (traveler_id);


--
-- Name: t2f_travel_5b1d2adf; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_travel_5b1d2adf ON chad.t2f_travel USING btree (section_id);


--
-- Name: t2f_travel_cc247b05; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_travel_cc247b05 ON chad.t2f_travel USING btree (office_id);


--
-- Name: t2f_travel_e2fa5388; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_travel_e2fa5388 ON chad.t2f_travel USING btree (created);


--
-- Name: t2f_travel_eae0a89e; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_travel_eae0a89e ON chad.t2f_travel USING btree (supervisor_id);


--
-- Name: t2f_travel_reference_number_42d9bee3_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_travel_reference_number_42d9bee3_like ON chad.t2f_travel USING btree (reference_number varchar_pattern_ops);


--
-- Name: t2f_travelactivity_4e98b6eb; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_travelactivity_4e98b6eb ON chad.t2f_travelactivity USING btree (partner_id);


--
-- Name: t2f_travelactivity_57f06544; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_travelactivity_57f06544 ON chad.t2f_travelactivity USING btree (result_id);


--
-- Name: t2f_travelactivity_7e0b0e70; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_travelactivity_7e0b0e70 ON chad.t2f_travelactivity USING btree (primary_traveler_id);


--
-- Name: t2f_travelactivity_cd976882; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_travelactivity_cd976882 ON chad.t2f_travelactivity USING btree (partnership_id);


--
-- Name: t2f_travelactivity_locations_931b52cf; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_travelactivity_locations_931b52cf ON chad.t2f_travelactivity_locations USING btree (travelactivity_id);


--
-- Name: t2f_travelactivity_locations_e274a5da; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_travelactivity_locations_e274a5da ON chad.t2f_travelactivity_locations USING btree (location_id);


--
-- Name: t2f_travelactivity_travels_46413c35; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_travelactivity_travels_46413c35 ON chad.t2f_travelactivity_travels USING btree (travel_id);


--
-- Name: t2f_travelactivity_travels_931b52cf; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_travelactivity_travels_931b52cf ON chad.t2f_travelactivity_travels USING btree (travelactivity_id);


--
-- Name: t2f_travelattachment_46413c35; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX t2f_travelattachment_46413c35 ON chad.t2f_travelattachment USING btree (travel_id);


--
-- Name: tpm_tpmactivity_10443b87; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX tpm_tpmactivity_10443b87 ON chad.tpm_tpmactivity USING btree (tpm_visit_id);


--
-- Name: tpm_tpmactivity_730f6511; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX tpm_tpmactivity_730f6511 ON chad.tpm_tpmactivity USING btree (section_id);


--
-- Name: tpm_tpmactivity_offices_6ddb34c5; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX tpm_tpmactivity_offices_6ddb34c5 ON chad.tpm_tpmactivity_offices USING btree (tpmactivity_id);


--
-- Name: tpm_tpmactivity_offices_cc247b05; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX tpm_tpmactivity_offices_cc247b05 ON chad.tpm_tpmactivity_offices USING btree (office_id);


--
-- Name: tpm_tpmactivity_unicef_focal_points_6ddb34c5; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX tpm_tpmactivity_unicef_focal_points_6ddb34c5 ON chad.tpm_tpmactivity_unicef_focal_points USING btree (tpmactivity_id);


--
-- Name: tpm_tpmactivity_unicef_focal_points_e8701ad4; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX tpm_tpmactivity_unicef_focal_points_e8701ad4 ON chad.tpm_tpmactivity_unicef_focal_points USING btree (user_id);


--
-- Name: tpm_tpmvisit_4f331e2f; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX tpm_tpmvisit_4f331e2f ON chad.tpm_tpmvisit USING btree (author_id);


--
-- Name: tpm_tpmvisit_b350ef8d; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX tpm_tpmvisit_b350ef8d ON chad.tpm_tpmvisit USING btree (tpm_partner_id);


--
-- Name: tpm_tpmvisit_tpm_partner_focal_points1_09c31592; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX tpm_tpmvisit_tpm_partner_focal_points1_09c31592 ON chad.tpm_tpmvisit_tpm_partner_focal_points USING btree (tpmvisit_id);


--
-- Name: tpm_tpmvisit_tpm_partner_focal_points1_18420715; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX tpm_tpmvisit_tpm_partner_focal_points1_18420715 ON chad.tpm_tpmvisit_tpm_partner_focal_points USING btree (tpmpartnerstaffmember_id);


--
-- Name: tpm_tpmvisitreportrejectcomment_10443b87; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX tpm_tpmvisitreportrejectcomment_10443b87 ON chad.tpm_tpmvisitreportrejectcomment USING btree (tpm_visit_id);


--
-- Name: unicef_snapshot_activity_1cd2a6ae; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX unicef_snapshot_activity_1cd2a6ae ON chad.unicef_snapshot_activity USING btree (target_object_id);


--
-- Name: unicef_snapshot_activity_1ef87b2e; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX unicef_snapshot_activity_1ef87b2e ON chad.unicef_snapshot_activity USING btree (by_user_id);


--
-- Name: unicef_snapshot_activity_e4f9dcc7; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX unicef_snapshot_activity_e4f9dcc7 ON chad.unicef_snapshot_activity USING btree (target_content_type_id);


--
-- Name: unicef_snapshot_activity_target_object_id_0b5e771f_like; Type: INDEX; Schema: chad; Owner: -
--

CREATE INDEX unicef_snapshot_activity_target_object_id_0b5e771f_like ON chad.unicef_snapshot_activity USING btree (target_object_id varchar_pattern_ops);


--
-- Name: partners_agreement_authorized_officers D15e05615b6a65add8b09843bc7c0bc1; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_agreement_authorized_officers
    ADD CONSTRAINT "D15e05615b6a65add8b09843bc7c0bc1" FOREIGN KEY (partnerstaffmember_id) REFERENCES chad.partners_partnerstaffmember(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_interventionresultlink_ram_indicators D29183ec8762f668cefd3b157f3df814; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionresultlink_ram_indicators
    ADD CONSTRAINT "D29183ec8762f668cefd3b157f3df814" FOREIGN KEY (interventionresultlink_id) REFERENCES chad.partners_interventionresultlink(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_intervention_partner_focal_points D49030e13108e81ef56369acd87f4420; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_partner_focal_points
    ADD CONSTRAINT "D49030e13108e81ef56369acd87f4420" FOREIGN KEY (partnerstaffmember_id) REFERENCES chad.partners_partnerstaffmember(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_engagement_authorized_officers D82fb6f801c2dbc1a882337e5dafab6d; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_engagement_authorized_officers
    ADD CONSTRAINT "D82fb6f801c2dbc1a882337e5dafab6d" FOREIGN KEY (partnerstaffmember_id) REFERENCES chad.partners_partnerstaffmember(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: actstream_action D8c098335a5d7c94956e9f6d80fbc74d; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.actstream_action
    ADD CONSTRAINT "D8c098335a5d7c94956e9f6d80fbc74d" FOREIGN KEY (action_object_content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_detailedfindinginfo a2e59fbbbca4df12e18a82ca9b1a2437; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_detailedfindinginfo
    ADD CONSTRAINT a2e59fbbbca4df12e18a82ca9b1a2437 FOREIGN KEY (micro_assesment_id) REFERENCES chad.audit_microassessment(engagement_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: action_points_actionpoint act_tpm_activity_id_f070575a_fk_tpm_tpmactivity_activity_ptr_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.action_points_actionpoint
    ADD CONSTRAINT act_tpm_activity_id_f070575a_fk_tpm_tpmactivity_activity_ptr_id FOREIGN KEY (tpm_activity_id) REFERENCES chad.tpm_tpmactivity(activity_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: action_points_actionpoint action_p_partner_id_f681df85_fk_partners_partnerorganization_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.action_points_actionpoint
    ADD CONSTRAINT action_p_partner_id_f681df85_fk_partners_partnerorganization_id FOREIGN KEY (partner_id) REFERENCES chad.partners_partnerorganization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: action_points_actionpoint action_poi_intervention_id_55242b43_fk_partners_intervention_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.action_points_actionpoint
    ADD CONSTRAINT action_poi_intervention_id_55242b43_fk_partners_intervention_id FOREIGN KEY (intervention_id) REFERENCES chad.partners_intervention(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: action_points_actionpoint action_poi_travel_activity_id_67662b24_fk_t2f_travelactivity_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.action_points_actionpoint
    ADD CONSTRAINT action_poi_travel_activity_id_67662b24_fk_t2f_travelactivity_id FOREIGN KEY (travel_activity_id) REFERENCES chad.t2f_travelactivity(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: action_points_actionpoint action_points_ac_category_id_b36e1bb5_fk_categories_category_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.action_points_actionpoint
    ADD CONSTRAINT action_points_ac_category_id_b36e1bb5_fk_categories_category_id FOREIGN KEY (category_id) REFERENCES public.categories_category(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: action_points_actionpoint action_points_act_engagement_id_33b5b13f_fk_audit_engagement_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.action_points_actionpoint
    ADD CONSTRAINT action_points_act_engagement_id_33b5b13f_fk_audit_engagement_id FOREIGN KEY (engagement_id) REFERENCES chad.audit_engagement(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: action_points_actionpoint action_points_act_location_id_ee07cdb0_fk_locations_location_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.action_points_actionpoint
    ADD CONSTRAINT action_points_act_location_id_ee07cdb0_fk_locations_location_id FOREIGN KEY (location_id) REFERENCES chad.locations_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: action_points_actionpoint action_points_action_cp_output_id_206572a6_fk_reports_result_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.action_points_actionpoint
    ADD CONSTRAINT action_points_action_cp_output_id_206572a6_fk_reports_result_id FOREIGN KEY (cp_output_id) REFERENCES chad.reports_result(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: action_points_actionpoint action_points_actionpo_section_id_26cf0900_fk_reports_sector_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.action_points_actionpoint
    ADD CONSTRAINT action_points_actionpo_section_id_26cf0900_fk_reports_sector_id FOREIGN KEY (section_id) REFERENCES chad.reports_sector(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: action_points_actionpoint action_points_actionpoi_assigned_by_id_bc6026e5_fk_auth_user_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.action_points_actionpoint
    ADD CONSTRAINT action_points_actionpoi_assigned_by_id_bc6026e5_fk_auth_user_id FOREIGN KEY (assigned_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: action_points_actionpoint action_points_actionpoi_assigned_to_id_ef25393b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.action_points_actionpoint
    ADD CONSTRAINT action_points_actionpoi_assigned_to_id_ef25393b_fk_auth_user_id FOREIGN KEY (assigned_to_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: action_points_actionpoint action_points_actionpoint_author_id_62635fb4_fk_auth_user_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.action_points_actionpoint
    ADD CONSTRAINT action_points_actionpoint_author_id_62635fb4_fk_auth_user_id FOREIGN KEY (author_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: action_points_actionpoint action_points_actionpoint_office_id_8247345a_fk_users_office_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.action_points_actionpoint
    ADD CONSTRAINT action_points_actionpoint_office_id_8247345a_fk_users_office_id FOREIGN KEY (office_id) REFERENCES public.users_office(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: activities_activity activiti_partner_id_b1e71c7f_fk_partners_partnerorganization_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.activities_activity
    ADD CONSTRAINT activiti_partner_id_b1e71c7f_fk_partners_partnerorganization_id FOREIGN KEY (partner_id) REFERENCES chad.partners_partnerorganization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: activities_activity_locations activities_activ_activity_id_33d34fdc_fk_activities_activity_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.activities_activity_locations
    ADD CONSTRAINT activities_activ_activity_id_33d34fdc_fk_activities_activity_id FOREIGN KEY (activity_id) REFERENCES chad.activities_activity(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: activities_activity_locations activities_activi_location_id_1678688a_fk_locations_location_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.activities_activity_locations
    ADD CONSTRAINT activities_activi_location_id_1678688a_fk_locations_location_id FOREIGN KEY (location_id) REFERENCES chad.locations_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: activities_activity activities_activity_cp_output_id_a915d1d3_fk_reports_result_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.activities_activity
    ADD CONSTRAINT activities_activity_cp_output_id_a915d1d3_fk_reports_result_id FOREIGN KEY (cp_output_id) REFERENCES chad.reports_result(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: activities_activity activities_intervention_id_7ba52d0e_fk_partners_intervention_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.activities_activity
    ADD CONSTRAINT activities_intervention_id_7ba52d0e_fk_partners_intervention_id FOREIGN KEY (intervention_id) REFERENCES chad.partners_intervention(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: actstream_action actst_target_content_type_id_187fa164_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.actstream_action
    ADD CONSTRAINT actst_target_content_type_id_187fa164_fk_django_content_type_id FOREIGN KEY (target_content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: actstream_action actstr_actor_content_type_id_d5e5ec2a_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.actstream_action
    ADD CONSTRAINT actstr_actor_content_type_id_d5e5ec2a_fk_django_content_type_id FOREIGN KEY (actor_content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: actstream_follow actstream_fo_content_type_id_ba287eb9_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.actstream_follow
    ADD CONSTRAINT actstream_fo_content_type_id_ba287eb9_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: actstream_follow actstream_follow_user_id_e9d4e1ff_fk_auth_user_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.actstream_follow
    ADD CONSTRAINT actstream_follow_user_id_e9d4e1ff_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_intervention adeb7d74fe49f7effa312e47f7981645; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention
    ADD CONSTRAINT adeb7d74fe49f7effa312e47f7981645 FOREIGN KEY (partner_authorized_officer_signatory_id) REFERENCES chad.partners_partnerstaffmember(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: attachments_attachment attachments__content_type_id_35dd9d5d_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.attachments_attachment
    ADD CONSTRAINT attachments__content_type_id_35dd9d5d_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: attachments_attachment attachments_at_file_type_id_9b87232b_fk_attachments_filetype_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.attachments_attachment
    ADD CONSTRAINT attachments_at_file_type_id_9b87232b_fk_attachments_filetype_id FOREIGN KEY (file_type_id) REFERENCES chad.attachments_filetype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: attachments_attachmentflat attachments_attachment_id_f44b472a_fk_attachments_attachment_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.attachments_attachmentflat
    ADD CONSTRAINT attachments_attachment_id_f44b472a_fk_attachments_attachment_id FOREIGN KEY (attachment_id) REFERENCES chad.attachments_attachment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: attachments_attachment attachments_attachment_uploaded_by_id_17a1c093_fk_auth_user_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.attachments_attachment
    ADD CONSTRAINT attachments_attachment_uploaded_by_id_17a1c093_fk_auth_user_id FOREIGN KEY (uploaded_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_finding aud_spot_check_id_0a087ac9_fk_audit_spotcheck_engagement_ptr_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_finding
    ADD CONSTRAINT aud_spot_check_id_0a087ac9_fk_audit_spotcheck_engagement_ptr_id FOREIGN KEY (spot_check_id) REFERENCES chad.audit_spotcheck(engagement_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_engagement audi_po_item_id_5da58b83_fk_purchase_order_purchaseorderitem_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_engagement
    ADD CONSTRAINT audi_po_item_id_5da58b83_fk_purchase_order_purchaseorderitem_id FOREIGN KEY (po_item_id) REFERENCES public.purchase_order_purchaseorderitem(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_engagement audit__agreement_id_3307176a_fk_purchase_order_purchaseorder_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_engagement
    ADD CONSTRAINT audit__agreement_id_3307176a_fk_purchase_order_purchaseorder_id FOREIGN KEY (agreement_id) REFERENCES public.purchase_order_purchaseorder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_audit audit_audit_engagement_ptr_id_44be495b_fk_audit_engagement_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_audit
    ADD CONSTRAINT audit_audit_engagement_ptr_id_44be495b_fk_audit_engagement_id FOREIGN KEY (engagement_ptr_id) REFERENCES chad.audit_engagement(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_specificprocedure audit_audit_id_a94bf354_fk_audit_specialaudit_engagement_ptr_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_specificprocedure
    ADD CONSTRAINT audit_audit_id_a94bf354_fk_audit_specialaudit_engagement_ptr_id FOREIGN KEY (audit_id) REFERENCES chad.audit_specialaudit(engagement_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_specialauditrecommendation audit_audit_id_d0ae73b3_fk_audit_specialaudit_engagement_ptr_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_specialauditrecommendation
    ADD CONSTRAINT audit_audit_id_d0ae73b3_fk_audit_specialaudit_engagement_ptr_id FOREIGN KEY (audit_id) REFERENCES chad.audit_specialaudit(engagement_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_engagement audit_en_partner_id_95e4e987_fk_partners_partnerorganization_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_engagement
    ADD CONSTRAINT audit_en_partner_id_95e4e987_fk_partners_partnerorganization_id FOREIGN KEY (partner_id) REFERENCES chad.partners_partnerorganization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_engagement_active_pd audit_enga_intervention_id_ad65e1a3_fk_partners_intervention_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_engagement_active_pd
    ADD CONSTRAINT audit_enga_intervention_id_ad65e1a3_fk_partners_intervention_id FOREIGN KEY (intervention_id) REFERENCES chad.partners_intervention(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_engagement_authorized_officers audit_engagement__engagement_id_190b3caf_fk_audit_engagement_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_engagement_authorized_officers
    ADD CONSTRAINT audit_engagement__engagement_id_190b3caf_fk_audit_engagement_id FOREIGN KEY (engagement_id) REFERENCES chad.audit_engagement(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_engagement_staff_members audit_engagement__engagement_id_210a7284_fk_audit_engagement_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_engagement_staff_members
    ADD CONSTRAINT audit_engagement__engagement_id_210a7284_fk_audit_engagement_id FOREIGN KEY (engagement_id) REFERENCES chad.audit_engagement(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_engagement_active_pd audit_engagement__engagement_id_94574f33_fk_audit_engagement_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_engagement_active_pd
    ADD CONSTRAINT audit_engagement__engagement_id_94574f33_fk_audit_engagement_id FOREIGN KEY (engagement_id) REFERENCES chad.audit_engagement(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_financialfinding audit_financ_audit_id_6abd6721_fk_audit_audit_engagement_ptr_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_financialfinding
    ADD CONSTRAINT audit_financ_audit_id_6abd6721_fk_audit_audit_engagement_ptr_id FOREIGN KEY (audit_id) REFERENCES chad.audit_audit(engagement_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_keyinternalcontrol audit_keyint_audit_id_e6cf0950_fk_audit_audit_engagement_ptr_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_keyinternalcontrol
    ADD CONSTRAINT audit_keyint_audit_id_e6cf0950_fk_audit_audit_engagement_ptr_id FOREIGN KEY (audit_id) REFERENCES chad.audit_audit(engagement_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_microassessment audit_microas_engagement_ptr_id_718a21a3_fk_audit_engagement_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_microassessment
    ADD CONSTRAINT audit_microas_engagement_ptr_id_718a21a3_fk_audit_engagement_id FOREIGN KEY (engagement_ptr_id) REFERENCES chad.audit_engagement(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_risk audit_risk_blueprint_id_53f54744_fk_audit_riskblueprint_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_risk
    ADD CONSTRAINT audit_risk_blueprint_id_53f54744_fk_audit_riskblueprint_id FOREIGN KEY (blueprint_id) REFERENCES chad.audit_riskblueprint(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_risk audit_risk_engagement_id_9545049c_fk_audit_engagement_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_risk
    ADD CONSTRAINT audit_risk_engagement_id_9545049c_fk_audit_engagement_id FOREIGN KEY (engagement_id) REFERENCES chad.audit_engagement(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_riskblueprint audit_riskbluepri_category_id_65dbb4ca_fk_audit_riskcategory_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_riskblueprint
    ADD CONSTRAINT audit_riskbluepri_category_id_65dbb4ca_fk_audit_riskcategory_id FOREIGN KEY (category_id) REFERENCES chad.audit_riskcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_riskcategory audit_riskcategory_parent_id_1e70c312_fk_audit_riskcategory_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_riskcategory
    ADD CONSTRAINT audit_riskcategory_parent_id_1e70c312_fk_audit_riskcategory_id FOREIGN KEY (parent_id) REFERENCES chad.audit_riskcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_specialaudit audit_special_engagement_ptr_id_d8f1bf74_fk_audit_engagement_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_specialaudit
    ADD CONSTRAINT audit_special_engagement_ptr_id_d8f1bf74_fk_audit_engagement_id FOREIGN KEY (engagement_ptr_id) REFERENCES chad.audit_engagement(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_spotcheck audit_spotche_engagement_ptr_id_7aad2e02_fk_audit_engagement_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_spotcheck
    ADD CONSTRAINT audit_spotche_engagement_ptr_id_7aad2e02_fk_audit_engagement_id FOREIGN KEY (engagement_ptr_id) REFERENCES chad.audit_engagement(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_comments django_comme_content_type_id_c4afe962_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.django_comments
    ADD CONSTRAINT django_comme_content_type_id_c4afe962_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_comment_flags django_comment_flags_comment_id_d8054933_fk_django_comments_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.django_comment_flags
    ADD CONSTRAINT django_comment_flags_comment_id_d8054933_fk_django_comments_id FOREIGN KEY (comment_id) REFERENCES chad.django_comments(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_comment_flags django_comment_flags_user_id_f3f81f0a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.django_comment_flags
    ADD CONSTRAINT django_comment_flags_user_id_f3f81f0a_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_comments django_comments_site_id_9dcf666e_fk_django_site_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.django_comments
    ADD CONSTRAINT django_comments_site_id_9dcf666e_fk_django_site_id FOREIGN KEY (site_id) REFERENCES public.django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_comments django_comments_user_id_a0a440a1_fk_auth_user_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.django_comments
    ADD CONSTRAINT django_comments_user_id_a0a440a1_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: funds_fundsreservationitem eddbdb3aee5d08e0b909e4a102354502; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_fundsreservationitem
    ADD CONSTRAINT eddbdb3aee5d08e0b909e4a102354502 FOREIGN KEY (fund_reservation_id) REFERENCES chad.funds_fundsreservationheader(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tpm_tpmvisit_tpm_partner_focal_points f086100a656c365c800dd0014a3a34f1; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmvisit_tpm_partner_focal_points
    ADD CONSTRAINT f086100a656c365c800dd0014a3a34f1 FOREIGN KEY (tpmpartnerstaffmember_id) REFERENCES public.tpmpartners_tpmpartnerstaffmember(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: audit_engagement_staff_members f2bd17555d7d671f284e1ba6c988713a; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.audit_engagement_staff_members
    ADD CONSTRAINT f2bd17555d7d671f284e1ba6c988713a FOREIGN KEY (auditorstaffmember_id) REFERENCES public.purchase_order_auditorstaffmember(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_interventionsectorlocationlink_locations f6e945cf3065e94fe6ff2dd810773eb9; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionsectorlocationlink_locations
    ADD CONSTRAINT f6e945cf3065e94fe6ff2dd810773eb9 FOREIGN KEY (interventionsectorlocationlink_id) REFERENCES chad.partners_interventionsectorlocationlink(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: funds_fundscommitmentitem f_fund_commitment_id_efde5c22_fk_funds_fundscommitmentheader_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_fundscommitmentitem
    ADD CONSTRAINT f_fund_commitment_id_efde5c22_fk_funds_fundscommitmentheader_id FOREIGN KEY (fund_commitment_id) REFERENCES chad.funds_fundscommitmentheader(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: funds_fundsreservationheader funds_fund_intervention_id_f4bb5671_fk_partners_intervention_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_fundsreservationheader
    ADD CONSTRAINT funds_fund_intervention_id_f4bb5671_fk_partners_intervention_id FOREIGN KEY (intervention_id) REFERENCES chad.partners_intervention(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: funds_grant funds_grant_donor_id_ad795503_fk_funds_donor_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.funds_grant
    ADD CONSTRAINT funds_grant_donor_id_ad795503_fk_funds_donor_id FOREIGN KEY (donor_id) REFERENCES chad.funds_donor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: hact_hacthistory hact_hac_partner_id_572719d9_fk_partners_partnerorganization_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.hact_hacthistory
    ADD CONSTRAINT hact_hac_partner_id_572719d9_fk_partners_partnerorganization_id FOREIGN KEY (partner_id) REFERENCES chad.partners_partnerorganization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_cartodbtable locations_carto_parent_id_c6ee9886_fk_locations_cartodbtable_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.locations_cartodbtable
    ADD CONSTRAINT locations_carto_parent_id_c6ee9886_fk_locations_cartodbtable_id FOREIGN KEY (parent_id) REFERENCES chad.locations_cartodbtable(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_location locations_locat_gateway_id_248fb7f2_fk_locations_gatewaytype_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.locations_location
    ADD CONSTRAINT locations_locat_gateway_id_248fb7f2_fk_locations_gatewaytype_id FOREIGN KEY (gateway_id) REFERENCES chad.locations_gatewaytype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_location locations_location_parent_id_d8d97084_fk_locations_location_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.locations_location
    ADD CONSTRAINT locations_location_parent_id_d8d97084_fk_locations_location_id FOREIGN KEY (parent_id) REFERENCES chad.locations_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_cartodbtable locations_location_type_id_92eab18c_fk_locations_gatewaytype_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.locations_cartodbtable
    ADD CONSTRAINT locations_location_type_id_92eab18c_fk_locations_gatewaytype_id FOREIGN KEY (location_type_id) REFERENCES chad.locations_gatewaytype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: management_flaggedissue management_f_content_type_id_0f13b2e7_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.management_flaggedissue
    ADD CONSTRAINT management_f_content_type_id_0f13b2e7_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_agreement p_partner_manager_id_e11fff68_fk_partners_partnerstaffmember_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_agreement
    ADD CONSTRAINT p_partner_manager_id_e11fff68_fk_partners_partnerstaffmember_id FOREIGN KEY (partner_manager_id) REFERENCES chad.partners_partnerstaffmember(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_intervention pa_country_programme_id_2bbfbdc4_fk_reports_countryprogramme_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention
    ADD CONSTRAINT pa_country_programme_id_2bbfbdc4_fk_reports_countryprogramme_id FOREIGN KEY (country_programme_id) REFERENCES chad.reports_countryprogramme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_agreement pa_country_programme_id_f666e6b3_fk_reports_countryprogramme_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_agreement
    ADD CONSTRAINT pa_country_programme_id_f666e6b3_fk_reports_countryprogramme_id FOREIGN KEY (country_programme_id) REFERENCES chad.reports_countryprogramme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_agreement_authorized_officers partners_agreeme_agreement_id_07d0dafd_fk_partners_agreement_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_agreement_authorized_officers
    ADD CONSTRAINT partners_agreeme_agreement_id_07d0dafd_fk_partners_agreement_id FOREIGN KEY (agreement_id) REFERENCES chad.partners_agreement(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_agreementamendment partners_agreeme_agreement_id_6b079e8c_fk_partners_agreement_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_agreementamendment
    ADD CONSTRAINT partners_agreeme_agreement_id_6b079e8c_fk_partners_agreement_id FOREIGN KEY (agreement_id) REFERENCES chad.partners_agreement(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_agreement partners_agreement_signed_by_id_3d7272a5_fk_auth_user_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_agreement
    ADD CONSTRAINT partners_agreement_signed_by_id_3d7272a5_fk_auth_user_id FOREIGN KEY (signed_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_assessment partners_assessm_requesting_officer_id_606627d7_fk_auth_user_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_assessment
    ADD CONSTRAINT partners_assessm_requesting_officer_id_606627d7_fk_auth_user_id FOREIGN KEY (requesting_officer_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_assessment partners_assessme_approving_officer_id_811c2fdd_fk_auth_user_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_assessment
    ADD CONSTRAINT partners_assessme_approving_officer_id_811c2fdd_fk_auth_user_id FOREIGN KEY (approving_officer_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_fundingcommitment partners_fundingcommitment_grant_id_83ea245d_fk_funds_grant_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_fundingcommitment
    ADD CONSTRAINT partners_fundingcommitment_grant_id_83ea245d_fk_funds_grant_id FOREIGN KEY (grant_id) REFERENCES chad.funds_grant(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_intervention_partner_focal_points partners_i_intervention_id_104c89ac_fk_partners_intervention_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_partner_focal_points
    ADD CONSTRAINT partners_i_intervention_id_104c89ac_fk_partners_intervention_id FOREIGN KEY (intervention_id) REFERENCES chad.partners_intervention(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_interventionattachment partners_i_intervention_id_3235c54c_fk_partners_intervention_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionattachment
    ADD CONSTRAINT partners_i_intervention_id_3235c54c_fk_partners_intervention_id FOREIGN KEY (intervention_id) REFERENCES chad.partners_intervention(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_interventionbudget partners_i_intervention_id_4b2f53ff_fk_partners_intervention_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionbudget
    ADD CONSTRAINT partners_i_intervention_id_4b2f53ff_fk_partners_intervention_id FOREIGN KEY (intervention_id) REFERENCES chad.partners_intervention(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_interventionsectorlocationlink partners_i_intervention_id_4bad99f5_fk_partners_intervention_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionsectorlocationlink
    ADD CONSTRAINT partners_i_intervention_id_4bad99f5_fk_partners_intervention_id FOREIGN KEY (intervention_id) REFERENCES chad.partners_intervention(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_intervention_flat_locations partners_i_intervention_id_4de66d52_fk_partners_intervention_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_flat_locations
    ADD CONSTRAINT partners_i_intervention_id_4de66d52_fk_partners_intervention_id FOREIGN KEY (intervention_id) REFERENCES chad.partners_intervention(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_interventionamendment partners_i_intervention_id_80b9b8d9_fk_partners_intervention_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionamendment
    ADD CONSTRAINT partners_i_intervention_id_80b9b8d9_fk_partners_intervention_id FOREIGN KEY (intervention_id) REFERENCES chad.partners_intervention(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_intervention_offices partners_i_intervention_id_9e1a86b1_fk_partners_intervention_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_offices
    ADD CONSTRAINT partners_i_intervention_id_9e1a86b1_fk_partners_intervention_id FOREIGN KEY (intervention_id) REFERENCES chad.partners_intervention(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_intervention_unicef_focal_points partners_i_intervention_id_a29eb115_fk_partners_intervention_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_unicef_focal_points
    ADD CONSTRAINT partners_i_intervention_id_a29eb115_fk_partners_intervention_id FOREIGN KEY (intervention_id) REFERENCES chad.partners_intervention(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_interventionreportingperiod partners_i_intervention_id_c3532d63_fk_partners_intervention_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionreportingperiod
    ADD CONSTRAINT partners_i_intervention_id_c3532d63_fk_partners_intervention_id FOREIGN KEY (intervention_id) REFERENCES chad.partners_intervention(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_intervention_sections partners_i_intervention_id_c7247d3d_fk_partners_intervention_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_sections
    ADD CONSTRAINT partners_i_intervention_id_c7247d3d_fk_partners_intervention_id FOREIGN KEY (intervention_id) REFERENCES chad.partners_intervention(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_interventionplannedvisits partners_i_intervention_id_ea9dfc78_fk_partners_intervention_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionplannedvisits
    ADD CONSTRAINT partners_i_intervention_id_ea9dfc78_fk_partners_intervention_id FOREIGN KEY (intervention_id) REFERENCES chad.partners_intervention(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_interventionresultlink partners_i_intervention_id_f10550d3_fk_partners_intervention_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionresultlink
    ADD CONSTRAINT partners_i_intervention_id_f10550d3_fk_partners_intervention_id FOREIGN KEY (intervention_id) REFERENCES chad.partners_intervention(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_intervention partners_interve_agreement_id_261b055d_fk_partners_agreement_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention
    ADD CONSTRAINT partners_interve_agreement_id_261b055d_fk_partners_agreement_id FOREIGN KEY (agreement_id) REFERENCES chad.partners_agreement(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_interventionresultlink_ram_indicators partners_interven_indicator_id_39b85ee5_fk_reports_indicator_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionresultlink_ram_indicators
    ADD CONSTRAINT partners_interven_indicator_id_39b85ee5_fk_reports_indicator_id FOREIGN KEY (indicator_id) REFERENCES chad.reports_indicator(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_interventionsectorlocationlink_locations partners_interven_location_id_454c4337_fk_locations_location_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionsectorlocationlink_locations
    ADD CONSTRAINT partners_interven_location_id_454c4337_fk_locations_location_id FOREIGN KEY (location_id) REFERENCES chad.locations_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_intervention_flat_locations partners_interven_location_id_50504821_fk_locations_location_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_flat_locations
    ADD CONSTRAINT partners_interven_location_id_50504821_fk_locations_location_id FOREIGN KEY (location_id) REFERENCES chad.locations_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_intervention partners_intervent_unicef_signatory_id_bb864e26_fk_auth_user_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention
    ADD CONSTRAINT partners_intervent_unicef_signatory_id_bb864e26_fk_auth_user_id FOREIGN KEY (unicef_signatory_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_interventionresultlink partners_interventio_cp_output_id_c5c9c310_fk_reports_result_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionresultlink
    ADD CONSTRAINT partners_interventio_cp_output_id_c5c9c310_fk_reports_result_id FOREIGN KEY (cp_output_id) REFERENCES chad.reports_result(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_intervention_offices partners_intervention_off_office_id_9db4b723_fk_users_office_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_offices
    ADD CONSTRAINT partners_intervention_off_office_id_9db4b723_fk_users_office_id FOREIGN KEY (office_id) REFERENCES public.users_office(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_intervention_sections partners_intervention_s_sector_id_f77679e8_fk_reports_sector_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_sections
    ADD CONSTRAINT partners_intervention_s_sector_id_f77679e8_fk_reports_sector_id FOREIGN KEY (sector_id) REFERENCES chad.reports_sector(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_intervention_unicef_focal_points partners_intervention_unicef_f_user_id_fc575e61_fk_auth_user_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_intervention_unicef_focal_points
    ADD CONSTRAINT partners_intervention_unicef_f_user_id_fc575e61_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_interventionattachment partners_interventiona_type_id_a73b39dd_fk_partners_filetype_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionattachment
    ADD CONSTRAINT partners_interventiona_type_id_a73b39dd_fk_partners_filetype_id FOREIGN KEY (type_id) REFERENCES chad.partners_filetype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_interventionsectorlocationlink partners_interventionse_sector_id_3c5d6302_fk_reports_sector_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_interventionsectorlocationlink
    ADD CONSTRAINT partners_interventionse_sector_id_3c5d6302_fk_reports_sector_id FOREIGN KEY (sector_id) REFERENCES chad.reports_sector(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_plannedengagement partners_partner_id_2cdd2ebd_fk_partners_partnerorganization_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_plannedengagement
    ADD CONSTRAINT partners_partner_id_2cdd2ebd_fk_partners_partnerorganization_id FOREIGN KEY (partner_id) REFERENCES chad.partners_partnerorganization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_assessment partners_partner_id_3210a37c_fk_partners_partnerorganization_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_assessment
    ADD CONSTRAINT partners_partner_id_3210a37c_fk_partners_partnerorganization_id FOREIGN KEY (partner_id) REFERENCES chad.partners_partnerorganization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_corevaluesassessment partners_partner_id_3e1ad525_fk_partners_partnerorganization_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_corevaluesassessment
    ADD CONSTRAINT partners_partner_id_3e1ad525_fk_partners_partnerorganization_id FOREIGN KEY (partner_id) REFERENCES chad.partners_partnerorganization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_agreement partners_partner_id_73a9e5cb_fk_partners_partnerorganization_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_agreement
    ADD CONSTRAINT partners_partner_id_73a9e5cb_fk_partners_partnerorganization_id FOREIGN KEY (partner_id) REFERENCES chad.partners_partnerorganization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_partnerstaffmember partners_partner_id_d798f374_fk_partners_partnerorganization_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_partnerstaffmember
    ADD CONSTRAINT partners_partner_id_d798f374_fk_partners_partnerorganization_id FOREIGN KEY (partner_id) REFERENCES chad.partners_partnerorganization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partners_partnerplannedvisits partners_partner_id_dde73d25_fk_partners_partnerorganization_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.partners_partnerplannedvisits
    ADD CONSTRAINT partners_partner_id_dde73d25_fk_partners_partnerorganization_id FOREIGN KEY (partner_id) REFERENCES chad.partners_partnerorganization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reports_lowerresult r_result_link_id_7845851f_fk_partners_interventionresultlink_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_lowerresult
    ADD CONSTRAINT r_result_link_id_7845851f_fk_partners_interventionresultlink_id FOREIGN KEY (result_link_id) REFERENCES chad.partners_interventionresultlink(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reports_result re_country_programme_id_845c97db_fk_reports_countryprogramme_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_result
    ADD CONSTRAINT re_country_programme_id_845c97db_fk_reports_countryprogramme_id FOREIGN KEY (country_programme_id) REFERENCES chad.reports_countryprogramme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reports_appliedindicator_disaggregation rep_appliedindicator_id_122e3733_fk_reports_appliedindicator_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_appliedindicator_disaggregation
    ADD CONSTRAINT rep_appliedindicator_id_122e3733_fk_reports_appliedindicator_id FOREIGN KEY (appliedindicator_id) REFERENCES chad.reports_appliedindicator(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reports_appliedindicator_locations rep_appliedindicator_id_27192e01_fk_reports_appliedindicator_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_appliedindicator_locations
    ADD CONSTRAINT rep_appliedindicator_id_27192e01_fk_reports_appliedindicator_id FOREIGN KEY (appliedindicator_id) REFERENCES chad.reports_appliedindicator(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reports_appliedindicator reports__indicator_id_22487a91_fk_reports_indicatorblueprint_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_appliedindicator
    ADD CONSTRAINT reports__indicator_id_22487a91_fk_reports_indicatorblueprint_id FOREIGN KEY (indicator_id) REFERENCES chad.reports_indicatorblueprint(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reports_appliedindicator reports_appl_lower_result_id_37b6aba6_fk_reports_lowerresult_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_appliedindicator
    ADD CONSTRAINT reports_appl_lower_result_id_37b6aba6_fk_reports_lowerresult_id FOREIGN KEY (lower_result_id) REFERENCES chad.reports_lowerresult(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reports_appliedindicator_locations reports_appliedin_location_id_ae178643_fk_locations_location_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_appliedindicator_locations
    ADD CONSTRAINT reports_appliedin_location_id_ae178643_fk_locations_location_id FOREIGN KEY (location_id) REFERENCES chad.locations_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reports_appliedindicator reports_appliedindicat_section_id_f9efc19a_fk_reports_sector_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_appliedindicator
    ADD CONSTRAINT reports_appliedindicat_section_id_f9efc19a_fk_reports_sector_id FOREIGN KEY (section_id) REFERENCES chad.reports_sector(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reports_disaggregationvalue reports_disaggregation_id_1a2698b6_fk_reports_disaggregation_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_disaggregationvalue
    ADD CONSTRAINT reports_disaggregation_id_1a2698b6_fk_reports_disaggregation_id FOREIGN KEY (disaggregation_id) REFERENCES chad.reports_disaggregation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reports_appliedindicator_disaggregation reports_disaggregation_id_63a65708_fk_reports_disaggregation_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_appliedindicator_disaggregation
    ADD CONSTRAINT reports_disaggregation_id_63a65708_fk_reports_disaggregation_id FOREIGN KEY (disaggregation_id) REFERENCES chad.reports_disaggregation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reports_indicator reports_indicator_result_id_2481fb57_fk_reports_result_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_indicator
    ADD CONSTRAINT reports_indicator_result_id_2481fb57_fk_reports_result_id FOREIGN KEY (result_id) REFERENCES chad.reports_result(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reports_indicator reports_indicator_sector_id_597b00ac_fk_reports_sector_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_indicator
    ADD CONSTRAINT reports_indicator_sector_id_597b00ac_fk_reports_sector_id FOREIGN KEY (sector_id) REFERENCES chad.reports_sector(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reports_indicator reports_indicator_unit_id_7616f859_fk_reports_unit_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_indicator
    ADD CONSTRAINT reports_indicator_unit_id_7616f859_fk_reports_unit_id FOREIGN KEY (unit_id) REFERENCES chad.reports_unit(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reports_reportingrequirement reports_re_intervention_id_830cca37_fk_partners_intervention_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_reportingrequirement
    ADD CONSTRAINT reports_re_intervention_id_830cca37_fk_partners_intervention_id FOREIGN KEY (intervention_id) REFERENCES chad.partners_intervention(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reports_result reports_result_parent_id_bf10f168_fk_reports_result_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_result
    ADD CONSTRAINT reports_result_parent_id_bf10f168_fk_reports_result_id FOREIGN KEY (parent_id) REFERENCES chad.reports_result(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reports_result reports_result_result_type_id_f8664ca6_fk_reports_resulttype_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_result
    ADD CONSTRAINT reports_result_result_type_id_f8664ca6_fk_reports_resulttype_id FOREIGN KEY (result_type_id) REFERENCES chad.reports_resulttype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reports_result reports_result_sector_id_62cb3e6e_fk_reports_sector_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_result
    ADD CONSTRAINT reports_result_sector_id_62cb3e6e_fk_reports_sector_id FOREIGN KEY (sector_id) REFERENCES chad.reports_sector(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reports_specialreportingrequirement reports_sp_intervention_id_d9d797f5_fk_partners_intervention_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reports_specialreportingrequirement
    ADD CONSTRAINT reports_sp_intervention_id_d9d797f5_fk_partners_intervention_id FOREIGN KEY (intervention_id) REFERENCES chad.partners_intervention(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reversion_revision reversion_revision_user_id_17095f45_fk_auth_user_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reversion_revision
    ADD CONSTRAINT reversion_revision_user_id_17095f45_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reversion_version reversion_ve_content_type_id_7d0ff25c_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reversion_version
    ADD CONSTRAINT reversion_ve_content_type_id_7d0ff25c_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reversion_version reversion_version_revision_id_af9f6a9d_fk_reversion_revision_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.reversion_version
    ADD CONSTRAINT reversion_version_revision_id_af9f6a9d_fk_reversion_revision_id FOREIGN KEY (revision_id) REFERENCES chad.reversion_revision(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: snapshot_activity snaps_target_content_type_id_9469a7c6_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.snapshot_activity
    ADD CONSTRAINT snaps_target_content_type_id_9469a7c6_fk_django_content_type_id FOREIGN KEY (target_content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: snapshot_activity snapshot_activity_by_user_id_cf2a78b9_fk_auth_user_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.snapshot_activity
    ADD CONSTRAINT snapshot_activity_by_user_id_cf2a78b9_fk_auth_user_id FOREIGN KEY (by_user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_actionpoint t2f_actionpoint_assigned_by_id_18063263_fk_auth_user_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_actionpoint
    ADD CONSTRAINT t2f_actionpoint_assigned_by_id_18063263_fk_auth_user_id FOREIGN KEY (assigned_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_actionpoint t2f_actionpoint_person_responsible_id_6d9abaa1_fk_auth_user_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_actionpoint
    ADD CONSTRAINT t2f_actionpoint_person_responsible_id_6d9abaa1_fk_auth_user_id FOREIGN KEY (person_responsible_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_actionpoint t2f_actionpoint_travel_id_3d959197_fk_t2f_travel_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_actionpoint
    ADD CONSTRAINT t2f_actionpoint_travel_id_3d959197_fk_t2f_travel_id FOREIGN KEY (travel_id) REFERENCES chad.t2f_travel(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_clearances t2f_clearances_travel_id_6ca8aeda_fk_t2f_travel_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_clearances
    ADD CONSTRAINT t2f_clearances_travel_id_6ca8aeda_fk_t2f_travel_id FOREIGN KEY (travel_id) REFERENCES chad.t2f_travel(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_costassignment t2f_costas_business_area_id_0cf80dcc_fk_publics_businessarea_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_costassignment
    ADD CONSTRAINT t2f_costas_business_area_id_0cf80dcc_fk_publics_businessarea_id FOREIGN KEY (business_area_id) REFERENCES public.publics_businessarea(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_costassignment t2f_costassignment_fund_id_8a802f1c_fk_publics_fund_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_costassignment
    ADD CONSTRAINT t2f_costassignment_fund_id_8a802f1c_fk_publics_fund_id FOREIGN KEY (fund_id) REFERENCES public.publics_fund(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_costassignment t2f_costassignment_grant_id_632638aa_fk_publics_grant_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_costassignment
    ADD CONSTRAINT t2f_costassignment_grant_id_632638aa_fk_publics_grant_id FOREIGN KEY (grant_id) REFERENCES public.publics_grant(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_costassignment t2f_costassignment_travel_id_514de7d8_fk_t2f_travel_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_costassignment
    ADD CONSTRAINT t2f_costassignment_travel_id_514de7d8_fk_t2f_travel_id FOREIGN KEY (travel_id) REFERENCES chad.t2f_travel(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_costassignment t2f_costassignment_wbs_id_ccbf7cc7_fk_publics_wbs_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_costassignment
    ADD CONSTRAINT t2f_costassignment_wbs_id_ccbf7cc7_fk_publics_wbs_id FOREIGN KEY (wbs_id) REFERENCES public.publics_wbs(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_deduction t2f_deduction_travel_id_3da7902a_fk_t2f_travel_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_deduction
    ADD CONSTRAINT t2f_deduction_travel_id_3da7902a_fk_t2f_travel_id FOREIGN KEY (travel_id) REFERENCES chad.t2f_travel(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_expense t2f_expense_currency_id_1ab5089a_fk_publics_currency_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_expense
    ADD CONSTRAINT t2f_expense_currency_id_1ab5089a_fk_publics_currency_id FOREIGN KEY (currency_id) REFERENCES public.publics_currency(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_expense t2f_expense_travel_id_16af434c_fk_t2f_travel_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_expense
    ADD CONSTRAINT t2f_expense_travel_id_16af434c_fk_t2f_travel_id FOREIGN KEY (travel_id) REFERENCES chad.t2f_travel(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_expense t2f_expense_type_id_8e999744_fk_publics_travelexpensetype_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_expense
    ADD CONSTRAINT t2f_expense_type_id_8e999744_fk_publics_travelexpensetype_id FOREIGN KEY (type_id) REFERENCES public.publics_travelexpensetype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_invoice t2f_invoice_currency_id_ce7cb7a3_fk_publics_currency_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_invoice
    ADD CONSTRAINT t2f_invoice_currency_id_ce7cb7a3_fk_publics_currency_id FOREIGN KEY (currency_id) REFERENCES public.publics_currency(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_invoice t2f_invoice_travel_id_905f65ab_fk_t2f_travel_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_invoice
    ADD CONSTRAINT t2f_invoice_travel_id_905f65ab_fk_t2f_travel_id FOREIGN KEY (travel_id) REFERENCES chad.t2f_travel(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_invoiceitem t2f_invoiceitem_fund_id_6187cb54_fk_publics_fund_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_invoiceitem
    ADD CONSTRAINT t2f_invoiceitem_fund_id_6187cb54_fk_publics_fund_id FOREIGN KEY (fund_id) REFERENCES public.publics_fund(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_invoiceitem t2f_invoiceitem_grant_id_cb6bb8f6_fk_publics_grant_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_invoiceitem
    ADD CONSTRAINT t2f_invoiceitem_grant_id_cb6bb8f6_fk_publics_grant_id FOREIGN KEY (grant_id) REFERENCES public.publics_grant(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_invoiceitem t2f_invoiceitem_invoice_id_5e1603cd_fk_t2f_invoice_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_invoiceitem
    ADD CONSTRAINT t2f_invoiceitem_invoice_id_5e1603cd_fk_t2f_invoice_id FOREIGN KEY (invoice_id) REFERENCES chad.t2f_invoice(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_invoiceitem t2f_invoiceitem_wbs_id_5c58fb45_fk_publics_wbs_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_invoiceitem
    ADD CONSTRAINT t2f_invoiceitem_wbs_id_5c58fb45_fk_publics_wbs_id FOREIGN KEY (wbs_id) REFERENCES public.publics_wbs(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_itineraryitem_airlines t2f_ite_airlinecompany_id_9af18782_fk_publics_airlinecompany_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_itineraryitem_airlines
    ADD CONSTRAINT t2f_ite_airlinecompany_id_9af18782_fk_publics_airlinecompany_id FOREIGN KEY (airlinecompany_id) REFERENCES public.publics_airlinecompany(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_itineraryitem t2f_iteneraryitem_travel_id_5c66d05a_fk_t2f_travel_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_itineraryitem
    ADD CONSTRAINT t2f_iteneraryitem_travel_id_5c66d05a_fk_t2f_travel_id FOREIGN KEY (travel_id) REFERENCES chad.t2f_travel(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_itineraryitem_airlines t2f_itinerary_itineraryitem_id_7b99ad96_fk_t2f_itineraryitem_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_itineraryitem_airlines
    ADD CONSTRAINT t2f_itinerary_itineraryitem_id_7b99ad96_fk_t2f_itineraryitem_id FOREIGN KEY (itineraryitem_id) REFERENCES chad.t2f_itineraryitem(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_itineraryitem t2f_itineraryite_dsa_region_id_701176f5_fk_publics_dsaregion_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_itineraryitem
    ADD CONSTRAINT t2f_itineraryite_dsa_region_id_701176f5_fk_publics_dsaregion_id FOREIGN KEY (dsa_region_id) REFERENCES public.publics_dsaregion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_travelactivity t2f_trav_partner_id_30a33a39_fk_partners_partnerorganization_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travelactivity
    ADD CONSTRAINT t2f_trav_partner_id_30a33a39_fk_partners_partnerorganization_id FOREIGN KEY (partner_id) REFERENCES chad.partners_partnerorganization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_travel t2f_travel_currency_id_abad886d_fk_publics_currency_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travel
    ADD CONSTRAINT t2f_travel_currency_id_abad886d_fk_publics_currency_id FOREIGN KEY (currency_id) REFERENCES public.publics_currency(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_travel t2f_travel_office_id_5dacac5a_fk_users_office_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travel
    ADD CONSTRAINT t2f_travel_office_id_5dacac5a_fk_users_office_id FOREIGN KEY (office_id) REFERENCES public.users_office(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_travel t2f_travel_section_id_6cae723c_fk_reports_sector_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travel
    ADD CONSTRAINT t2f_travel_section_id_6cae723c_fk_reports_sector_id FOREIGN KEY (section_id) REFERENCES chad.reports_sector(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_travel t2f_travel_supervisor_id_eeae00f1_fk_auth_user_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travel
    ADD CONSTRAINT t2f_travel_supervisor_id_eeae00f1_fk_auth_user_id FOREIGN KEY (supervisor_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_travel t2f_travel_traveler_id_64920fcd_fk_auth_user_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travel
    ADD CONSTRAINT t2f_travel_traveler_id_64920fcd_fk_auth_user_id FOREIGN KEY (traveler_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_travelactivity t2f_travela_partnership_id_e15d5db1_fk_partners_intervention_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travelactivity
    ADD CONSTRAINT t2f_travela_partnership_id_e15d5db1_fk_partners_intervention_id FOREIGN KEY (partnership_id) REFERENCES chad.partners_intervention(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_travelactivity_travels t2f_travela_travelactivity_id_689cd1f4_fk_t2f_travelactivity_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travelactivity_travels
    ADD CONSTRAINT t2f_travela_travelactivity_id_689cd1f4_fk_t2f_travelactivity_id FOREIGN KEY (travelactivity_id) REFERENCES chad.t2f_travelactivity(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_travelactivity_locations t2f_travela_travelactivity_id_e0d80da2_fk_t2f_travelactivity_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travelactivity_locations
    ADD CONSTRAINT t2f_travela_travelactivity_id_e0d80da2_fk_t2f_travelactivity_id FOREIGN KEY (travelactivity_id) REFERENCES chad.t2f_travelactivity(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_travelactivity_locations t2f_travelactivit_location_id_4557e829_fk_locations_location_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travelactivity_locations
    ADD CONSTRAINT t2f_travelactivit_location_id_4557e829_fk_locations_location_id FOREIGN KEY (location_id) REFERENCES chad.locations_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_travelactivity t2f_travelactivity_primary_traveler_id_1fec2059_fk_auth_user_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travelactivity
    ADD CONSTRAINT t2f_travelactivity_primary_traveler_id_1fec2059_fk_auth_user_id FOREIGN KEY (primary_traveler_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_travelactivity t2f_travelactivity_result_id_f793e65f_fk_reports_result_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travelactivity
    ADD CONSTRAINT t2f_travelactivity_result_id_f793e65f_fk_reports_result_id FOREIGN KEY (result_id) REFERENCES chad.reports_result(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_travelactivity_travels t2f_travelactivity_travels_travel_id_27d022c6_fk_t2f_travel_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travelactivity_travels
    ADD CONSTRAINT t2f_travelactivity_travels_travel_id_27d022c6_fk_t2f_travel_id FOREIGN KEY (travel_id) REFERENCES chad.t2f_travel(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: t2f_travelattachment t2f_travelattachment_travel_id_e8d90898_fk_t2f_travel_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.t2f_travelattachment
    ADD CONSTRAINT t2f_travelattachment_travel_id_e8d90898_fk_t2f_travel_id FOREIGN KEY (travel_id) REFERENCES chad.t2f_travel(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tpm_tpmactivity_unicef_focal_points tpm__tpmactivity_id_29a0c70a_fk_tpm_tpmactivity_activity_ptr_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmactivity_unicef_focal_points
    ADD CONSTRAINT tpm__tpmactivity_id_29a0c70a_fk_tpm_tpmactivity_activity_ptr_id FOREIGN KEY (tpmactivity_id) REFERENCES chad.tpm_tpmactivity(activity_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tpm_tpmactivity_offices tpm__tpmactivity_id_760ccefe_fk_tpm_tpmactivity_activity_ptr_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmactivity_offices
    ADD CONSTRAINT tpm__tpmactivity_id_760ccefe_fk_tpm_tpmactivity_activity_ptr_id FOREIGN KEY (tpmactivity_id) REFERENCES chad.tpm_tpmactivity(activity_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tpm_tpmactivity tpm_tpmactiv_activity_ptr_id_3ca6cc19_fk_activities_activity_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmactivity
    ADD CONSTRAINT tpm_tpmactiv_activity_ptr_id_3ca6cc19_fk_activities_activity_id FOREIGN KEY (activity_ptr_id) REFERENCES chad.activities_activity(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tpm_tpmactivity_offices tpm_tpmactivity_offices_office_id_b388619e_fk_users_office_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmactivity_offices
    ADD CONSTRAINT tpm_tpmactivity_offices_office_id_b388619e_fk_users_office_id FOREIGN KEY (office_id) REFERENCES public.users_office(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tpm_tpmactivity tpm_tpmactivity_section_id_5512c079_fk_reports_sector_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmactivity
    ADD CONSTRAINT tpm_tpmactivity_section_id_5512c079_fk_reports_sector_id FOREIGN KEY (section_id) REFERENCES chad.reports_sector(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tpm_tpmactivity tpm_tpmactivity_tpm_visit_id_32d33435_fk_tpm_tpmvisit_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmactivity
    ADD CONSTRAINT tpm_tpmactivity_tpm_visit_id_32d33435_fk_tpm_tpmvisit_id FOREIGN KEY (tpm_visit_id) REFERENCES chad.tpm_tpmvisit(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tpm_tpmactivity_unicef_focal_points tpm_tpmactivity_unicef_focal_p_user_id_f2e4e790_fk_auth_user_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmactivity_unicef_focal_points
    ADD CONSTRAINT tpm_tpmactivity_unicef_focal_p_user_id_f2e4e790_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tpm_tpmvisit tpm_tpmvis_tpm_partner_id_975d031e_fk_tpmpartners_tpmpartner_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmvisit
    ADD CONSTRAINT tpm_tpmvis_tpm_partner_id_975d031e_fk_tpmpartners_tpmpartner_id FOREIGN KEY (tpm_partner_id) REFERENCES public.tpmpartners_tpmpartner(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tpm_tpmvisit tpm_tpmvisit_author_id_6fe6b4c8_fk_auth_user_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmvisit
    ADD CONSTRAINT tpm_tpmvisit_author_id_6fe6b4c8_fk_auth_user_id FOREIGN KEY (author_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tpm_tpmvisit_tpm_partner_focal_points tpm_tpmvisit_tpm_partne_tpmvisit_id_a80f03b4_fk_tpm_tpmvisit_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmvisit_tpm_partner_focal_points
    ADD CONSTRAINT tpm_tpmvisit_tpm_partne_tpmvisit_id_a80f03b4_fk_tpm_tpmvisit_id FOREIGN KEY (tpmvisit_id) REFERENCES chad.tpm_tpmvisit(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tpm_tpmvisitreportrejectcomment tpm_tpmvisitreportreje_tpm_visit_id_633519f7_fk_tpm_tpmvisit_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.tpm_tpmvisitreportrejectcomment
    ADD CONSTRAINT tpm_tpmvisitreportreje_tpm_visit_id_633519f7_fk_tpm_tpmvisit_id FOREIGN KEY (tpm_visit_id) REFERENCES chad.tpm_tpmvisit(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: unicef_snapshot_activity unice_target_content_type_id_bec3e35f_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.unicef_snapshot_activity
    ADD CONSTRAINT unice_target_content_type_id_bec3e35f_fk_django_content_type_id FOREIGN KEY (target_content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: unicef_snapshot_activity unicef_snapshot_activity_by_user_id_c033a3d8_fk_auth_user_id; Type: FK CONSTRAINT; Schema: chad; Owner: -
--

ALTER TABLE ONLY chad.unicef_snapshot_activity
    ADD CONSTRAINT unicef_snapshot_activity_by_user_id_c033a3d8_fk_auth_user_id FOREIGN KEY (by_user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

