CREATE TABLE public.apps_web_service
(
   user_web character varying(255), 
   valido boolean, 
   password character varying(255), 
   ip character varying(255), 
   port integer, 
   id serial primary key
) 
WITH (
  OIDS = FALSE
)
;
ALTER TABLE public.apps_web_service
  OWNER TO django;
