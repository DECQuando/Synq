import imgsim
from django import forms
from django.db.models import Max

from .models import Image
from Synq.settings import BASE_DIR
import cv2


def calculate_distance(path1: str, path2: str) -> float:
    """
    2つの画像のベクトル間の距離を算出する関数
    :param path1: Path for the first image
    :param path2: Path for the second image
    :return: Vector distance between two images
    """
    # pathから画像データを取得
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)
    # imgsimライブラリで画像をベクトル化
    vtr = imgsim.Vectorizer()
    vec1 = vtr.vectorize(img1)
    vec2 = vtr.vectorize(img2)
    # 2つのベクトル間の距離を算出
    dist = imgsim.distance(vec1, vec2)
    return dist


def return_group(previous_image_group: int, distance: float, max_distance: int) -> int:
    """
    グループの番号を返す関数
    :param previous_image_group: Group of the previous image
    :param distance: Vector distance between two images
    :param max_distance: Maximum distance to be considered as the same group
    :return: Group number of the uploaded image
    """
    if distance <= max_distance:
        print("same: ", previous_image_group)
        print("dist: ", distance)
        return previous_image_group
    else:
        new_image_group = fetch_new_group()
        print("next: ", new_image_group)
        print("dist: ", distance)
        return new_image_group


def is_same_group(uploaded_image_group: int, latest_group: int) -> bool:
    """
    アップロードされた画像が新規グループか既存グループの画像か判定する関数
    :param uploaded_image_group: Group of uploaded image
    :param latest_group: Group of previous image
    :return: bool
    """
    if uploaded_image_group == latest_group:
        # 既存グループの画像
        return True
    else:
        # 新規グループの画像
        return False


def fetch_new_group() -> int:
    """
    新規グループの番号を返す関数
    :return: int
    """
    # DB全体で最後に作られたグループの投稿データを取得
    latest_group_data = Image.objects.filter(
        group=Image.objects.aggregate(Max('group'))['group__max']
    ).first()
    # 最新のグループを取得
    latest_group = latest_group_data.group
    new_group = latest_group + 1

    return new_group


def variance_of_laplacian(path: str) -> float:
    """
    compute the Laplacian of the image and then return the focus
    measure, which is simply the variance of the Laplacian
    :param path: Path for the image
    :return: sharpness
    """
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
    # 小数点以下3桁に丸めて返す
    return round(sharpness, 3)


def select_best_shot(group_id: int) -> None:
    """
    ベストショットを選択・記録する関数
    :param group_id:
    :return: None
    """
    obj = Image.objects.filter(group=group_id)

    # グループ中のベストショットの有無を確認(新規グループ作成時は存在しないため分岐必須)
    if obj.filter(is_best_shot=True).exists():
        # 元々のベストショットのフラグを消去する
        obj.filter(is_best_shot=True).update(is_best_shot=None)

    # 新しくベストショットのフラグを付与する
    obj_new_best_shot = obj.filter(
        edge_sharpness=obj.aggregate(Max('edge_sharpness'))['edge_sharpness__max']
    ).first()
    obj_new_best_shot.is_best_shot = True
    obj_new_best_shot.save()
    return None


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        # ユーザーに入力を許可するフィールドをfieldsで指定する
        fields = ("name", "image")

    def save(self, *args, **kwargs):
        obj = super(ImageForm, self).save(commit=False)

        # フォームからユーザーIDを取得し格納
        obj.user_id = obj.user.id

        # DBにデータが存在するか確認
        db_is_empty = not Image.objects.exists()
        if db_is_empty:  # データが存在しない場合のガード節
            # DBに一旦保存
            # 画像がまだ登録されていないときはgroup=1
            obj.group = 1
            obj.save()

            # 投稿された画像のパスを取得
            img_uploaded_path = str(BASE_DIR) + obj.image.url
            # sharpnessを計算
            obj.edge_sharpness = variance_of_laplacian(img_uploaded_path)
            obj.save()

            return obj

        # 以降はDBに既にデータが存在する場合(exists()==True)の処理

        # ユーザーの一つ前の投稿データを取得
        latest_user_data = Image.objects.filter(user_id=obj.user.id).latest('created_at')
        # ユーザーの一つ前の投稿のグループを取得
        latest_user_group = latest_user_data.group

        # DBに一旦保存
        obj.group = latest_user_group
        obj.save()

        # 投稿された画像のパスを取得
        img_uploaded_path = str(BASE_DIR) + obj.image.url
        # sharpnessを計算
        obj.edge_sharpness = variance_of_laplacian(img_uploaded_path)

        # 一つ前の画像データを取得
        img_latest_path = str(BASE_DIR) + latest_user_data.image.url
        dist = calculate_distance(path1=img_latest_path, path2=img_uploaded_path)
        group = return_group(
            previous_image_group=latest_user_group,
            distance=dist, max_distance=10
        )
        obj.group = group
        obj.save()

        # 新規グループの画像でない場合ベストショットを選出
        if is_same_group(group, latest_user_group):
            select_best_shot(group)

        return obj
