"""Service de parcours de la hiérarchie organisationnelle."""

from collections import deque
from typing import Dict, List, Set, Tuple
from .models import OrgNode, User
from .ports import UserRepository


class OrganizationService:
    """Parcourt l'arborescence managériale via un BFS."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_full_hierarchy(self, manager_name: str) -> List[OrgNode]:
        """Retourne toute la hiérarchie sous un manager (parcours BFS).

        Chaque utilisateur est encapsulé dans un OrgNode avec son niveau
        et le lien vers son manager direct. Un set évite les doublons.
        """
        manager = self.repository.find_by_name(manager_name)
        root = OrgNode(user=manager, level=0)

        seen: Set[str] = {manager.id}
        queue: deque[Tuple[str, int]] = deque([(manager.id, 0)])
        users_by_id: Dict[str, User] = {manager.id: manager}
        results: List[OrgNode] = [root]

        while queue:
            current_id, current_level = queue.popleft()
            current_user = users_by_id[current_id]

            for user in self.repository.get_direct_reports(current_id):
                if user.id not in seen:
                    seen.add(user.id)
                    users_by_id[user.id] = user
                    results.append(OrgNode(
                        user=user,
                        level=current_level + 1,
                        manager_id=current_id,
                        manager_display_name=current_user.display_name,
                    ))
                    queue.append((user.id, current_level + 1))

        return results
