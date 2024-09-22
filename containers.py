import pydantic
from dependency_injector import containers, providers

from app.repositories import CompatibilityTarotResultRepository, TarotRepository
from app.services import TarotService
from app.utils import AnthropicProcessor
from configs import ApplicationSettings
from databases import Database


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            'app.routers',
        ],
    )
    config = providers.Configuration()
    config.from_dict(ApplicationSettings().model_dump())

    db = providers.Singleton(
        Database,
        db_url=config.db.url,
    )

    anthropic_processor = providers.Factory(
        AnthropicProcessor,
        api_key=config.claude_api_key,
    )
    
    tarot_repository = providers.Factory(
        TarotRepository,
        db=db,
    )
    compatibility_tarot_result_repository = providers.Factory(
        CompatibilityTarotResultRepository,
        db=db,
    )
    tarot_service = providers.Factory(
        TarotService,
        tarot_repository=tarot_repository,
        compatibility_tarot_result_repository=compatibility_tarot_result_repository,
        processor=anthropic_processor,
    )
