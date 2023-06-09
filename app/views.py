
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer, StudentSerializer, TeacherSerializer, SubjectSerializer, SubjectStudentSerializer
from .models import Student, Teacher, Subjects, StudentSubject
from rest_framework.generics import ListAPIView, ListCreateAPIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status


@api_view(['GET'])
def get_user_details(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


class StudentListView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TeacherListView(ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class SubjectListCreateAPIView(ListCreateAPIView):
    queryset = Subjects.objects.all()
    serializer_class = SubjectSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
        except RuntimeError as e:
            print(f"An error occurred: {e}")
            return Response(
                {"message": "An error occurred while creating the subject."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return response


class TeacherSubjectsListAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            teacher = request.user.teacher
            subjects = Subjects.objects.filter(teacher=teacher)
            serializer = SubjectSerializer(subjects, many=True)
            return Response(serializer.data)
        except AttributeError:
            return Response(
                {"message": "You are not authorized to view this resource."},
                status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            return Response(
                {"message": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SubjectStudentsListAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, subject_id):
        try:
            # Get the subject by subject_id
            subject = Subjects.objects.get(pk=subject_id)
            students = Student.objects.filter(studentsubject__subject=subject)
            serializer = StudentSerializer(students, many=True)

            return Response(serializer.data)
        except Subjects.DoesNotExist:
            return Response(
                {"message": "Subject not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"message": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class StudentScoreViews(APIView):
    def get(self, request, subject_id):
        subject = get_object_or_404(Subjects, pk=subject_id)
        student_subjects = StudentSubject.objects.filter(subject=subject)
        serializer = SubjectStudentSerializer(student_subjects, many=True)
        return Response(serializer.data)


    def patch(self, request, subject_id):
        subject = get_object_or_404(Subjects, pk=subject_id)
        student_id = int(request.data.get('student_id'))
        test_score = int(request.data.get('test_score'))  # Get the updated test score

        student = get_object_or_404(Student, user__id=student_id)
        student_subject = get_object_or_404(
            StudentSubject, subject=subject, student=student)  


        student_subject.test_score = test_score
        student_subject.save()

        serializer = SubjectStudentSerializer(
            student_subject, data=request.data, partial=True)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class StudentScoresAPIView(ListAPIView):
    serializer_class = SubjectStudentSerializer


    def get_queryset(self):
        user = self.request.user
        student = Student.objects.get(user=user)  # Assuming Student model has a 'user' field
        return StudentSubject.objects.filter(student=student)