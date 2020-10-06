psql -c "create user wedding with password 'W€dd1ngShop';"
createdb test_the_wedding_shop -Owedding -Ttemplate0
chmod +x tests/scripts/wedding_demo_data.sh
tests/scripts/wedding_demo_data.sh
psql -d test_the_wedding_shop -c "grant all privileges on all tables in schema public to wedding; alter default privileges in schema public grant all on tables to wedding;" -U postgres
sleep 2
tox