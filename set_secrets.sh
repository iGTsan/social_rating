head /dev/random | tr -dc 'A-Za-z0-9' | head -c 12 > POSTGRES_PW.txt
# docker secret create POSTGRES_PW POSTGRES_PW.txt

echo "your_vk_api_token" > VK_API_TOKEN.txt
echo "your_group_id" > VK_GROUP_ID.txt
# docker secret create VK_API_TOKEN VK_API_TOKEN.txt
# docker secret create VK_GROUP_ID VK_GROUP_ID.txt

echo "your_tg_api_token" > TG_API_TOKEN.txt
# docker secret create TG_API_TOKEN TG_API_TOKEN.txt
