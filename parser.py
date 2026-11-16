import asyncio
from loguru import logger
import httpx
from bs4 import BeautifulSoup

async def fetch_procurement_ge_tenders():

    url = "https://tenders.procurement.gov.ge/" 
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                logger.error(f"Ошибка получения данных: статус {response.status_code}")
                raise Exception(f"HTTP Error {response.status_code}")
            
            soup = BeautifulSoup(response.text, "html.parser")
            tenders_found = []
            
            return tenders_found
            
    except httpx.RequestError as e:
        logger.error(f"Сетевая ошибка при подключенни до procurement.gov.ge: {e}")
        raise e