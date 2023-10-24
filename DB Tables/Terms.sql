-- Table: public.Terms

-- DROP TABLE IF EXISTS public."Terms";

CREATE TABLE IF NOT EXISTS public."Terms"
(
    term_id integer NOT NULL,
    term text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Terms_pkey" PRIMARY KEY (term_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Terms"
    OWNER to postgres;