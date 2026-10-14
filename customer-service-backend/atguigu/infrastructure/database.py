import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine,async_sessionmaker
from atguigu.conf.config import settings

#定义全局的异步session工厂(engine)
#定义全局的session工厂
engine:AsyncEngine | None = None
async_session: async_sessionmaker[AsyncSession] | None = None

#初始化数据库连接资源
def init_db_engine():

    global engine,async_session
    #先创建引擎
    engine = create_async_engine(
        settings.database_url,
        echo=True, #打印sql语句
        pool_pre_ping=True, #每次从数据库连接池取出连接之前，先向数据库发送一个心跳请求，若数据库短暂失联可以反复发送心跳请求，若链接已断开则自动丢弃并创建新连接，避免连接失效的错误
    )

    #再由引擎创建session
    async_session =  async_sessionmaker(engine,expire_on_commit=False)

#关闭资源
async def close_db_engine():
    if engine is not None:
        await engine.dispose()

if __name__ == "__main__":
    async def test():
        #初始化引擎
        init_db_engine()

        #获取session对象
        async with async_session() as session:
            result = await session.execute(text("SELECT 1"))

            data_all = result.fetchall()
            print(data_all)
            data_one = result.fetchone()
        #关闭引擎
        await close_db_engine()

    asyncio.run(test())


#使用sessopm访问远程数据库