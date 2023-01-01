from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentSubmitSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources',__name__)

@teacher_assignments_resources.route('/assignments',methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    assignments_for_teacher = Assignment.get_assignments_for_teacher(p.teacher_id)
    teacher_assignment_dump = AssignmentSchema().dump(assignments_for_teacher, many=True)
    return APIResponse.respond(data=teacher_assignment_dump)

@teacher_assignments_resources.route('/assignments/grade',methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignments(p, incoming_payload):
    graded_assignment = Assignment.update_grade(incoming_payload['id'], incoming_payload['grade'], p)
    db.session.commit()
    upserted_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=upserted_assignment_dump)
