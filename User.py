import re


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.followers = set()
        self.posts = []
        self.notifications = []

    def validate_password(self, password):
        if password != self.password:
            return False
        else:
            return True

    def signup(username, password):
        User(username, password)

    def follow(self, other_user):
        other_user.followers.add(self)
        print(f"{self.username} started following {other_user.username}")

    def publish_post(self, contenttype, *args):
        from Post import Post
        from Post import SalePost
        if contenttype == "Text" and len(args) == 1:
            post = Post(self, "Text", args[0])
            product_details = f'{self.username} published a post:\n"{args[0]}"\n'
            print(f"{product_details}")
        elif contenttype == "Image" and len(args) == 1:
            post = Post(self, "Image", args[0])
            product_details = f"{self.username} posted a picture\n"
            print(f"{product_details}")
        elif contenttype == "Sale" and len(args) == 3:
            product_details = f"For sale! {args[0]}, price: {args[1]}, pickup from: {args[2]}"
            post = SalePost(self, args[0], args[1], args[2])
            print(f"{self.username} posted a product for sale:\n{product_details}\n")
        else:
            # Default to a generic post
            post = Post(contenttype, args[0] if args else None, self)

        self.posts.append(post)
        for follower in self.followers:
            follower.notifications.append(f"{self.username} has a new post")

        return post  # Return the created post

    def post_content(self, content_type, content):
        self.posts.append(f"User posted {content_type}: {content}")

    def process_notifications(self):
        for notification in self.notifications:
            print(f"Notification to {self.username}: {notification}")
        self.notifications = []

    def interact_with_post(self, other_user, interaction_type, interaction_content=None):
        interaction_message = f"notification to {other_user}: {self.username} {interaction_type} your post:"
        if interaction_content:
            interaction_message = f"notification to {other_user}: {self.username} {interaction_type} on your post:"
            interaction_message += f": {interaction_content}"
            other_user.notifications.append(interaction_message)

        other_user.notifications.append(interaction_message)

    def unfollow(self, other_user):
        for user in other_user.followers:
            if user == self:
                other_user.followers.remove(user)
                other_user.notifications.append(f"{self.username} unfollowed you")
                print(f"{self.username} unfollowed {other_user.username}")
                break

    def disconnect(self):
        print(f"{self.username} disconnected")

    def connect(self):
        print(f"{self.username} connected")

    def __str__(self):
        return f"User name: {self.username}, Number of posts: {len(self.posts)}, Number of followers: {len(self.followers)}"

    def print_notifications(self):
        print(f"{self.username}'s notifications:")
        for notification in self.notifications:
            print(f"{notification}")

    def extractusername(self, text1):
        text = text1
        # Define a regular expression pattern to match the username
        pattern = r"User name: (\w+),"
        # Use re.search to find the match
        match = re.search(pattern, text)
        # Extract the username from the match
        if match:
            username = match.group(1)
            return username
        else:
            return text
