import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column
from datetime import datetime, timezone
from datetime import date as date_doc


class Base(DeclarativeBase):
    pass


class SpimexTradingResult(Base):
    __tablename__ = 'spimex_trading_results'

    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_product_id: Mapped[str] = mapped_column()
    exchange_product_name: Mapped[str] = mapped_column()
    oil_id: Mapped[str] = mapped_column()
    delivery_basis_id: Mapped[str] = mapped_column()
    delivery_type_id: Mapped[str] = mapped_column()
    delivery_basis_name: Mapped[str] = mapped_column()
    volume: Mapped[int] = mapped_column()
    total: Mapped[int] = mapped_column()
    count: Mapped[int] = mapped_column()
    date: Mapped[date_doc] = mapped_column()
    created_on: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_on: Mapped[datetime] = mapped_column(default=None, nullable=True)


class BulletinPipeline:

    def open_spider(self, spider):
        engine = create_engine('sqlite:///sqlite_oil.db')
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        file_path = item['file_path']
        df = pd.read_excel(file_path, header=None)
        header_row = df[df.apply(lambda row: row.astype(str).str.contains('Метрическая тонна').any(), axis=1)].index[0]
        res_df = pd.read_excel(file_path, header=header_row+2)

        date_doc = item['date']
        date = datetime.strptime(date_doc, '%Y%m%d').date()
        
        for index in range(100000):
            rows = res_df.iloc[index].to_list()
            if rows[1] in ('Итого:', 'Итого: ', ' Итого:', 'Итого по секции:'):
                break
            if rows[14] == '-':
                continue
            new_oil = SpimexTradingResult(
                exchange_product_id=rows[1],
                exchange_product_name=rows[2],
                oil_id=rows[1][:4],
                delivery_basis_id=rows[1][4:7],
                delivery_basis_name=rows[3],
                delivery_type_id=rows[1][-1],
                volume=rows[4],
                total=rows[5],
                count=rows[14],
                date=date
            )
            self.session.add(new_oil)
        self.session.commit()
        return item
    
    def close_spider(self, spider):
        self.session.close()