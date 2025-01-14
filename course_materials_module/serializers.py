from rest_framework import serializers
from .models import CourseMaterial
from urllib.parse import urlparse


class CourseMaterialSerializer(serializers.ModelSerializer):
    course_id = serializers.UUIDField()
    course_name = serializers.CharField(source="course.course_name", read_only=True)  
    school_id = serializers.UUIDField()
    school_name = serializers.CharField(source="school.school_name", read_only=True)

    class Meta:
        model = CourseMaterial
        fields = ["course_material_id",
                  "course_material_name",
                  "course_material_file",
                  "course_id",
                    "course_name",
                  "school_id",
                    "school_name"
                  ]
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove query parameters from course_material_file URL
        course_material_file_url = data.get("course_material_file", "")
        parsed_url = urlparse(course_material_file_url)
        scheme_netloc_path = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
        data["course_material_file"] = scheme_netloc_path

        return data


