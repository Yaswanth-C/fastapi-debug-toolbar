from __future__ import annotations

import typing as t
from contextlib import AsyncExitStack

from fastapi import HTTPException, Request
from fastapi.dependencies.utils import solve_dependencies


async def get_dependencies(request: Request) -> dict[str, t.Any] | None:
    route = request["route"]

    if hasattr(route, "dependant"):
        try:
            if (
                "fastapi_inner_astack" not in request.scope
                or "fastapi_function_astack" not in request.scope
            ):
                async with AsyncExitStack() as request_stack:
                    request.scope["fastapi_inner_astack"] = request_stack
                    async with AsyncExitStack() as function_stack:
                        request.scope["fastapi_function_astack"] = function_stack
                        solved_result = await solve_dependencies(
                            request=request,
                            dependant=route.dependant,
                            dependency_overrides_provider=route.dependency_overrides_provider,
                            async_exit_stack=request_stack,
                            embed_body_fields=False,
                        )
            else:
                solved_result = await solve_dependencies(
                    request=request,
                    dependant=route.dependant,
                    dependency_overrides_provider=route.dependency_overrides_provider,
                    async_exit_stack=request.scope.get("fastapi_inner_astack"),
                    embed_body_fields=False,
                )
        except HTTPException:
            pass
        else:
            return solved_result.values
    return None
