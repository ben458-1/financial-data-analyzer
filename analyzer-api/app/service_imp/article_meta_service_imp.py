from typing import List, Optional, Dict

from app.db.session import DatabaseSession
from app.schemas.article_meta import ConfigModel
from app.service.article_meta_service import ArticleMetaConfigService
from app.db.dependency import get_db


class ArticleMetaConfigServiceImp(ArticleMetaConfigService):
    def create(self, config: ConfigModel) -> ConfigModel:
        pass

    def read(self, config_id: int) -> Optional[ConfigModel]:
        pass

    def update(self, config_id: int, config: ConfigModel) -> ConfigModel:
        pass

    def delete(self, config_id: int) -> None:
        pass

    def list(self) -> List[ConfigModel]:
        pass

    def find_all_by_newspaper_id(self, newspaper_id: int) -> List[ConfigModel]:
        with DatabaseSession() as db:
            query = "SELECT * FROM conf.articlesearchconf WHERE newspaper_id = %s"
            rows = db.fetch_all(query, (newspaper_id,))
            return [ConfigModel(**row) for row in rows]

    def aggregate_by_section(self, newspaper_id: int) -> Dict[str, List[ConfigModel]]:
        conf_list = self.find_all_by_newspaper_id(newspaper_id)
        conf_section_dict: Dict[str, List[ConfigModel]] = {}

        for conf in conf_list:
            section = conf.doc.articleSection
            conf_section_dict.setdefault(section, []).append(conf)

        return conf_section_dict
