#
#  Copyright 2024 The InfiniFlow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import json
import time
from typing import Any, cast

from langfuse import Langfuse

from api.db.services.canvas_service import UserCanvasService
from api.db.services.langfuse_service import TenantLangfuseService
from api.db.services.user_canvas_version import UserCanvasVersionService
from api.settings import RetCode
from api.utils import get_uuid
from api.utils.api_utils import get_data_error_result, get_error_data_result, get_json_result, token_required
from api.utils.api_utils import get_result
from flask import request

@manager.route('/agents', methods=['GET'])  # noqa: F821
@token_required
def list_agents(tenant_id):
    id = request.args.get("id")
    title = request.args.get("title")
    if id or title:
        canvas = UserCanvasService.query(id=id, title=title, user_id=tenant_id)
        if not canvas:
            return get_error_data_result("The agent doesn't exist.")
    page_number = int(request.args.get("page", 1))
    items_per_page = int(request.args.get("page_size", 30))
    orderby = request.args.get("orderby", "update_time")
    if request.args.get("desc") == "False" or request.args.get("desc") == "false":
        desc = False
    else:
        desc = True
    canvas = UserCanvasService.get_list(tenant_id,page_number,items_per_page,orderby,desc,id,title)
    return get_result(data=canvas)


@manager.route("/agents", methods=["POST"])  # noqa: F821
@token_required
def create_agent(tenant_id: str):
    req: dict[str, Any] = cast(dict[str, Any], request.json)
    req["user_id"] = tenant_id

    if req.get("dsl") is not None:
        if not isinstance(req["dsl"], str):
            req["dsl"] = json.dumps(req["dsl"], ensure_ascii=False)

        req["dsl"] = json.loads(req["dsl"])
    else:
        return get_json_result(data=False, message="No DSL data in request.", code=RetCode.ARGUMENT_ERROR)

    if req.get("title") is not None:
        req["title"] = req["title"].strip()
    else:
        return get_json_result(data=False, message="No title in request.", code=RetCode.ARGUMENT_ERROR)

    if UserCanvasService.query(user_id=tenant_id, title=req["title"]):
        return get_data_error_result(message=f"Agent with title {req['title']} already exists.")

    agent_id = get_uuid()
    req["id"] = agent_id

    if not UserCanvasService.save(**req):
        return get_data_error_result(message="Fail to create agent.")

    UserCanvasVersionService.insert(
        user_canvas_id=agent_id,
        title="{0}_{1}".format(req["title"], time.strftime("%Y_%m_%d_%H_%M_%S")),
        dsl=req["dsl"]
    )

    return get_json_result(data=True)


@manager.route("/agents/<agent_id>", methods=["PUT"])  # noqa: F821
@token_required
def update_agent(tenant_id: str, agent_id: str):
    req: dict[str, Any] = {k: v for k, v in cast(dict[str, Any], request.json).items() if v is not None}
    req["user_id"] = tenant_id

    if req.get("dsl") is not None:
        if not isinstance(req["dsl"], str):
            req["dsl"] = json.dumps(req["dsl"], ensure_ascii=False)

        req["dsl"] = json.loads(req["dsl"])
    
    if req.get("title") is not None:
        req["title"] = req["title"].strip()

    if not UserCanvasService.query(user_id=tenant_id, id=agent_id):
        return get_json_result(
            data=False, message="Only owner of canvas authorized for this operation.",
            code=RetCode.OPERATING_ERROR)

    UserCanvasService.update_by_id(agent_id, req)

    if req.get("dsl") is not None:
        UserCanvasVersionService.insert(
            user_canvas_id=agent_id,
            title="{0}_{1}".format(req["title"], time.strftime("%Y_%m_%d_%H_%M_%S")),
            dsl=req["dsl"]
        )

        UserCanvasVersionService.delete_all_versions(agent_id)

    return get_json_result(data=True)


@manager.route("/agents/<agent_id>", methods=["DELETE"])  # noqa: F821
@token_required
def delete_agent(tenant_id: str, agent_id: str):
    if not UserCanvasService.query(user_id=tenant_id, id=agent_id):
        return get_json_result(
            data=False, message="Only owner of canvas authorized for this operation.",
            code=RetCode.OPERATING_ERROR)

    UserCanvasService.delete_by_id(agent_id)
    return get_json_result(data=True)


@manager.route("/agents/annotate", methods=["POST"])  # noqa: F821
@token_required
def thumbs_up(tenant_id: str):
    req = request.json
    trace_id = req.get("trace_id")
    message_id = req.get("message_id")
    thumbs:bool = req.get("thumbs", False)
    langfuse_keys = TenantLangfuseService.filter_by_tenant(tenant_id=tenant_id)
    if not langfuse_keys:
        return get_json_result(message="Tenant config not found", code=404)

    langfuse = Langfuse(
        public_key=langfuse_keys.public_key,
        secret_key=langfuse_keys.secret_key,
        host=langfuse_keys.host
    )

    if not langfuse.auth_check():
        return get_json_result(message="Langfuse auth failed", code=403)

    try:
        trace = langfuse.fetch_trace(id=trace_id)
        observations = trace.data.observations

        # 查找 metadata 中带有 message_id 的 Observation
        matched_obs = next(
            (obs for obs in observations if obs.metadata.get("message_id") == message_id),
            None
        )

        if not matched_obs:
            return get_json_result(message="Observation not found", code=404)

        # 添加注解
        langfuse.score(
            trace_id=trace_id,
            observation_id=matched_obs.id,
            name="thumbs up down",
            value=thumbs,
            data_type="BOOLEAN"
        )

        return get_json_result(data='ok', message="Annotation added")

    except Exception as e:
        return get_json_result(message=f"Error: {str(e)}", code=404)
