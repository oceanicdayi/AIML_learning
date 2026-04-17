FROM nginx:alpine

# Copy only site-relevant files
COPY main.html /usr/share/nginx/html/index.html
COPY ai_tech_map_report.md /usr/share/nginx/html/
COPY anki_terms.csv /usr/share/nginx/html/
COPY readme.md /usr/share/nginx/html/
COPY README_HF.md /usr/share/nginx/html/
COPY Group*/ /usr/share/nginx/html/

# HF Spaces expects port 7860
ENV PORT=7860
RUN sed -i "s/listen\s*80;/listen 7860;/" /etc/nginx/conf.d/default.conf

EXPOSE 7860
