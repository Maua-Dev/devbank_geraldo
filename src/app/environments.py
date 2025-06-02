import os
from enum import Enum
from .repo.transaction_repository_interface import ITransactionsRepository
from .repo.user_repository_interface import IUserRepository
from .errors.environment_errors import EnvironmentNotFound


class STAGE(Enum):
    DOTENV = "DOTENV"
    DEV = "DEV"
    PROD = "PROD"
    TEST = "TEST"


class Environments:
    """
    Defines the environment variables for the application. You should not instantiate this class directly. Please use Environments.get_envs() method instead.

    Usage:

    """
    stage: STAGE

    def _configure_local(self):
        from dotenv import load_dotenv
        load_dotenv()
        os.environ["STAGE"] = os.environ.get("STAGE") or STAGE.TEST.value

    def load_envs(self):
        if "STAGE" not in os.environ or os.environ["STAGE"] == STAGE.DOTENV.value:
            self._configure_local()

        self.stage = STAGE[os.environ.get("STAGE")]
        
    @staticmethod
    def get_user_repo() -> IUserRepository:
        if Environments.get_envs().stage == STAGE.TEST:
            if Environments._user_repo_mock_instance is None:
                from .repo.user_repository_mock import UserRepositoryMock
                Environments._user_repo_mock_instance = UserRepositoryMock()
            return Environments._user_repo_mock_instance
        else:
            raise EnvironmentNotFound(f"User repo not configured for stage: {Environments.get_envs().stage}")
            
    @staticmethod
    def get_transaction_repo() -> ITransactionsRepository:
        if Environments.get_envs().stage == STAGE.TEST:
            if Environments._transaction_repo_mock_instance is None:
                from .repo.transaction_repository_mock import TransactionRepositoryMock
                Environments._transaction_repo_mock_instance = TransactionRepositoryMock()
            return Environments._transaction_repo_mock_instance
        else:
            raise EnvironmentNotFound(f"Transaction repo not configured for stage: {Environments.get_envs().stage}")

    @staticmethod
    def get_envs() -> "Environments":
        """
        Returns the Environments object. This method should be used to get the Environments object instead of instantiating it directly.
        :return: Environments (stage={self.stage})

        """
        envs = Environments()
        envs.load_envs()
        return envs

    def __repr__(self):
        return self.__dict__