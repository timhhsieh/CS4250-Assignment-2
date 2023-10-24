-- Table: public.Document Terms

-- DROP TABLE IF EXISTS public."Document Terms";

CREATE TABLE IF NOT EXISTS public."Document Terms"
(
    doc_id integer NOT NULL,
    term_id integer NOT NULL
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Document Terms"
    OWNER to postgres;