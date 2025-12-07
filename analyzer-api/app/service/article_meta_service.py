from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from app.schemas.article_meta import ConfigModel


class ArticleMetaConfigService(ABC):

    @abstractmethod
    def create(self, config: ConfigModel) -> ConfigModel:
        """Create a new ConfigModel entry."""
        pass

    @abstractmethod
    def read(self, config_id: int) -> Optional[ConfigModel]:
        """Retrieve a ConfigModel by its ID."""
        pass

    @abstractmethod
    def update(self, config_id: int, config: ConfigModel) -> ConfigModel:
        """Update an existing ConfigModel."""
        pass

    @abstractmethod
    def delete(self, config_id: int) -> None:
        """Delete a ConfigModel by its ID."""
        pass

    @abstractmethod
    def list(self) -> List[ConfigModel]:
        """List all ConfigModel entries."""
        pass

    @abstractmethod
    def find_all_by_newspaper_id(self, newspaper_id: int) -> List[ConfigModel]:
        pass

    @abstractmethod
    def aggregate_by_section(self, newspaper_id: int) -> Dict[str, List[ConfigModel]]:
        pass
