from flask import Flask, render_template, request, redirect, flash
import smtplib

app = Flask(__name__)
app.secret_key = "secretkey123"

# your Gmail info
YOUR_EMAIL = "Morenatlale10@gmail.com"
YOUR_PASSWORD = "lvrtdwvbpkyskvjq" 

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_email = request.form["email"]
        product = request.form["product"]

        subject = "New Product Request"
        message = f"User Email: {user_email}\nProduct: {product}"

        try:
            # send to you
            with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                smtp.starttls()
                smtp.login(YOUR_EMAIL, YOUR_PASSWORD)
                smtp.sendmail(YOUR_EMAIL, YOUR_EMAIL, f"Subject: {subject}\n\n{message}")
            print("Email sent to owner successfully.")

            # send confirmation to user
            confirmation_subject = "Order Received"
            confirmation_message = (
                "Thanks for your request!\nWe'll contact you soon about your product."
            )
            with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                smtp.starttls()
                smtp.login(YOUR_EMAIL, YOUR_PASSWORD)
                smtp.sendmail(
                    YOUR_EMAIL,
                    user_email,
                    f"Subject: {confirmation_subject}\n\n{confirmation_message}",
                )
            print("Confirmation email sent to user successfully.")
            flash("✅ Your request was received! Please check your email for confirmation.")
        except Exception as e:
            print("Error sending email:", e)
            flash("⚠️ Something went wrong. Please try again later.")

        return redirect("/")

    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)